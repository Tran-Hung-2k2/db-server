import Dagre from '@dagrejs/dagre';
import React, { useState, useRef, useCallback, useMemo } from 'react';
import ReactFlow, {
    ReactFlowProvider,
    addEdge,
    useNodesState,
    useEdgesState,
    Controls,
    Panel,
    useReactFlow,
    Background,
    BackgroundVariant,
    Position,
} from 'reactflow';
import 'reactflow/dist/style.css';
import FlowSidebar from '@components/FlowSidebar';
import { FiFile } from 'react-icons/fi';
import TurboNode from './TurboNode';
import TurboEdge from './TurboEdge';
import { PiExportBold } from 'react-icons/pi';
import { TbTransform } from 'react-icons/tb';
import { LuImport } from 'react-icons/lu';

// Initialize a Dagre graph with default edge labels
const dagreGraph = new Dagre.graphlib.Graph().setDefaultEdgeLabel(() => ({}));
// Function to layout nodes and edges using Dagre
const getLayoutedElements = (nodes, edges, options = { direction: 'TB' }) => {
    const isHorizontal = options.direction === 'LR';
    dagreGraph.setGraph({ rankdir: options.direction });

    edges.forEach((edge) => dagreGraph.setEdge(edge.source, edge.target));
    nodes.forEach((node) => dagreGraph.setNode(node.id, node));

    Dagre.layout(dagreGraph);

    nodes.forEach((node) => {
        const nodeWithPosition = dagreGraph.node(node.id);
        node.targetPosition = isHorizontal ? Position.Left : Position.Top;
        node.sourcePosition = isHorizontal ? Position.Right : Position.Bottom;

        node.position = {
            x: nodeWithPosition.x,
            y: nodeWithPosition.y,
        };

        return node;
    });

    return { nodes, edges };
};

// Helper function to generate unique IDs for new nodes
let id = 0;
const getId = () => `dndnode_${id++}`;

// Initial nodes and edges data
const initialNodes = [
    {
        id: '1',
        targetPosition: Position.Left,
        sourcePosition: Position.Right,
        position: { x: 0, y: 125 },
        data: { icon: <LuImport size={26} />, title: 'Data loader', subline: 'Kafka' },
        type: 'turbo',
    },
    {
        id: '2',
        targetPosition: Position.Left,
        sourcePosition: Position.Right,
        position: { x: 250, y: 125 },
        data: { icon: <TbTransform size={26} />, title: 'Transform', subline: 'Filter' },
        type: 'turbo',
    },
    {
        id: '5',
        targetPosition: Position.Left,
        sourcePosition: Position.Right,
        position: { x: 500, y: 125 },
        data: { icon: <PiExportBold size={26} />, title: 'Data eporter', subline: 'MinIO Delta' },
        type: 'turbo',
    },
];

const initialEdges = [
    { id: 'e1-2', source: '1', target: '2' },
    { id: 'e2-5', source: '2', target: '5' },
];

// Default options for edges
const defaultEdgeOptions = {
    type: 'turbo',
    markerEnd: 'edge-circle',
};

// Main component for the layout flow
const LayoutFlow = () => {
    const reactFlowWrapper = useRef(null);
    const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
    const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
    const [reactFlowInstance, setReactFlowInstance] = useState(null);
    const [variant, setVariant] = useState(BackgroundVariant.Dots);
    const { fitView } = useReactFlow();

    // Define custom node and edge types
    const nodeTypes = useMemo(
        () => ({
            turbo: TurboNode,
        }),
        [],
    );

    const edgeTypes = useMemo(
        () => ({
            turbo: TurboEdge,
        }),
        [],
    );

    // Handle new edge connections
    const onConnect = useCallback((params) => setEdges((eds) => addEdge(params, eds)), []);

    // Allow drag-over behavior
    const onDragOver = useCallback((event) => {
        event.preventDefault();
        event.dataTransfer.dropEffect = 'move';
    }, []);

    // Handle dropping new nodes onto the canvas
    const onDrop = useCallback(
        (event) => {
            event.preventDefault();
            const type = event.dataTransfer.getData('application/reactflow');
            if (typeof type === 'undefined' || !type) return;

            const position = reactFlowInstance.screenToFlowPosition({
                x: event.clientX,
                y: event.clientY,
            });

            let icon;

            if (type == 'Data loader') icon = <LuImport size={26} />;
            else if (type == 'Transformer') icon = <TbTransform size={26} />;
            else if (type == 'Data exporter') icon = <PiExportBold size={26} />;
            const newNode = {
                id: getId(),
                type: 'turbo',
                position,
                data: { icon: icon, title: 'My blocks name', subline: `${type}` },
            };
            setNodes((nds) => nds.concat(newNode));
        },
        [reactFlowInstance],
    );

    // Handle layout changes (direction)
    const onLayout = useCallback(
        (direction) => {
            const layouted = getLayoutedElements(nodes, edges, { direction });
            setNodes([...layouted.nodes]);
            setEdges([...layouted.edges]);
            window.requestAnimationFrame(() => {
                fitView();
            });
        },
        [nodes, edges],
    );

    return (
        <>
            {/* <FlowSidebar /> */}
            <div className="reactflow-wrapper" ref={reactFlowWrapper}>
                <ReactFlow
                    nodes={nodes}
                    edges={edges}
                    onNodesChange={onNodesChange}
                    onEdgesChange={onEdgesChange}
                    onConnect={onConnect}
                    onInit={setReactFlowInstance}
                    onDrop={onDrop}
                    onDragOver={onDragOver}
                    nodeTypes={nodeTypes}
                    edgeTypes={edgeTypes}
                    defaultEdgeOptions={defaultEdgeOptions}
                    fitView
                >
                    <Controls showInteractive={false} />
                    <Background color="#ddd" variant={variant} />
                    <Panel className="flex items-center gap-2">
                        <div className="font-bold">Kiểu nền:</div>
                        <button
                            className="text-white badge badge-success"
                            onClick={() => setVariant(BackgroundVariant.Dots)}
                        >
                            Dấu chấm
                        </button>
                        <button className="badge badge-warning" onClick={() => setVariant(BackgroundVariant.Lines)}>
                            Đường kẻ
                        </button>
                        <button
                            className="text-white badge badge-error"
                            onClick={() => setVariant(BackgroundVariant.Cross)}
                        >
                            Dấu cộng
                        </button>
                    </Panel>
                    <Panel position="top-right">
                        <div className="flex items-center gap-2">
                            <div className="font-bold">Sắp xếp:</div>
                            <button className="text-white badge badge-success" onClick={() => onLayout('TB')}>
                                Chiều dọc
                            </button>
                            <button className="text-white badge badge-success" onClick={() => onLayout('LR')}>
                                Chiều ngang
                            </button>
                        </div>
                    </Panel>
                    <svg>
                        <defs>
                            <linearGradient id="edge-gradient">
                                <stop offset="0%" stopColor="#ae53ba" />
                                <stop offset="100%" stopColor="#2a8af6" />
                            </linearGradient>
                            <marker
                                id="edge-circle"
                                viewBox="-5 -5 10 10"
                                refX="0"
                                refY="0"
                                markerUnits="strokeWidth"
                                markerWidth="10"
                                markerHeight="10"
                                orient="auto"
                            >
                                <circle stroke="#2a8af6" strokeOpacity="0.75" r="2" cx="0" cy="0" />
                            </marker>
                        </defs>
                    </svg>
                </ReactFlow>
            </div>
        </>
    );
};

// Main export component wrapped with ReactFlowProvider
export default function () {
    return (
        <div className="dndflow">
            <ReactFlowProvider>
                <LayoutFlow />
            </ReactFlowProvider>
        </div>
    );
}
