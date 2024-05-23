import React, { memo } from 'react';
import { Handle, Position } from 'reactflow';

export default memo(({ data, targetPosition, sourcePosition }) => {
    return (
        <>
            <div className="wrapper gradient">
                <div className="inner">
                    <div className="body">
                        {data.icon && <div className="icon">{data.icon}</div>}
                        <div>
                            <div className="title">{data.title}</div>
                            {data.subline && <div className="subline">{data.subline}</div>}
                        </div>
                    </div>
                    <Handle type="target" position={targetPosition ? targetPosition : Position.Left} />
                    <Handle type="source" position={sourcePosition ? sourcePosition : Position.Right} />
                </div>
            </div>
        </>
    );
});
