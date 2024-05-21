import Dagre from '@dagrejs/dagre';
import React, { useCallback, useState } from 'react';
import ReactFlow, {
    ReactFlowProvider,
    Panel,
    useNodesState,
    useEdgesState,
    useReactFlow,
    MiniMap,
    Controls,
    Background,
    BackgroundVariant,
} from 'reactflow';

import { initialNodes, initialEdges } from '@pages/nodes-edges.jsx';
import 'reactflow/dist/style.css';

const g = new Dagre.graphlib.Graph().setDefaultEdgeLabel(() => ({}));

const getLayoutedElements = (nodes, edges, options) => {
    g.setGraph({ rankdir: options.direction });

    edges.forEach((edge) => g.setEdge(edge.source, edge.target));
    nodes.forEach((node) => g.setNode(node.id, node));

    Dagre.layout(g);

    return {
        nodes: nodes.map((node) => {
            const { x, y } = g.node(node.id);

            return { ...node, position: { x, y } };
        }),
        edges,
    };
};

const LayoutFlow = () => {
    const { fitView } = useReactFlow();
    const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
    const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
    const [variant, setVariant] = useState(BackgroundVariant.Cross);

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
        <ReactFlow nodes={nodes} edges={edges} onNodesChange={onNodesChange} onEdgesChange={onEdgesChange} fitView>
            <MiniMap nodeStrokeWidth={3} zoomable pannable />
            <Controls />
            <Background color="#ccc" variant={variant} />
            <Panel className="flex items-center gap-2">
                <div className="font-bold">Kiểu nền:</div>
                <button className="text-white badge badge-success" onClick={() => setVariant(BackgroundVariant.Dots)}>
                    Dấu chấm
                </button>
                <button className="badge badge-warning" onClick={() => setVariant(BackgroundVariant.Lines)}>
                    Đường kẻ
                </button>
                <button className="text-white badge badge-error" onClick={() => setVariant(BackgroundVariant.Cross)}>
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
        </ReactFlow>
    );
};

export default function () {
    return (
        <ReactFlowProvider>
            <LayoutFlow />
        </ReactFlowProvider>
    );
}
