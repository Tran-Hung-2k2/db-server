import { useCallback, useState } from 'react';
import ReactFlow, {
    applyEdgeChanges,
    applyNodeChanges,
    addEdge,
    MiniMap,
    Controls,
    Background,
    Panel,
} from 'reactflow';
import 'reactflow/dist/style.css';
import Node from '@/components/Node';
import Egde from '@/components/Egde';

function Flow() {
    const [variant, setVariant] = useState('cross');
    const [nodes, setNodes] = useState(Node);
    const [edges, setEdges] = useState(Egde);

    const nodeColor = (node) => {
        switch (node.type) {
            case 'input':
                return '#6ede87';
            case 'output':
                return '#6865A5';
            default:
                return '#ff0072';
        }
    };

    const onNodeChange = useCallback((x) => setNodes((newNode) => applyNodeChanges(x, newNode)), [setNodes]);

    const onEdgeChange = useCallback((x) => setEdges((eds) => applyEdgeChanges(x, eds)), [setEdges]);

    const onEdgeConnect = useCallback((x) => setEdges((eds) => addEdge({ ...x, animated: true }, eds)), [setEdges]);

    return (
        <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodeChange}
            onEdgesChange={onEdgeChange}
            onConnect={onEdgeConnect}
            fitView
        >
            <MiniMap nodeColor={nodeColor} nodeStrokeWidth={3} zoomable pannable />
            <Controls />
            <Background color="#ccc" variant={variant} />
            <Panel className="flex items-center gap-2">
                <div className="font-bold">Kiểu nền:</div>
                <button className="text-white badge badge-success" onClick={() => setVariant('dots')}>
                    Dấu chấm
                </button>
                <button className="badge badge-warning" onClick={() => setVariant('lines')}>
                    Đường kẻ
                </button>
                <button className="text-white badge badge-error" onClick={() => setVariant('cross')}>
                    Dấu cộng
                </button>
            </Panel>
        </ReactFlow>
    );
}
export default Flow;
