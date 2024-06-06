import { Suspense, useEffect, useState } from 'react';
import { Route, Routes } from 'react-router-dom';

import routes from '@routes/index';

import RequireRole from '@components/RequireRole';
import Loader from '@components/Loader';

export default function App() {
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        setLoading(false);
    }, []);

    return loading ? (
        <Loader />
    ) : (
        <>
            <Routes>
                {routes.map((routeGroup, index) => {
                    const { require, layouts } = routeGroup;
                    return layouts.map((layoutGroup, layoutIndex) => {
                        const { layout: Layout, routes } = layoutGroup;
                        return routes.map((route, routeIndex) => {
                            const { path, component: Component, lazy } = route;
                            return (
                                <Route
                                    key={`${index}-${layoutIndex}-${routeIndex}`}
                                    path={path}
                                    element={
                                        require ? (
                                            <RequireRole roles={require}>
                                                {Layout ? (
                                                    <Layout>
                                                        <Suspense fallback={<Loader />}>
                                                            <Component />
                                                        </Suspense>
                                                    </Layout>
                                                ) : (
                                                    <Suspense fallback={<Loader />}>
                                                        <Component />
                                                    </Suspense>
                                                )}
                                            </RequireRole>
                                        ) : Layout ? (
                                            <Layout>
                                                <Suspense fallback={<Loader />}>
                                                    <Component />
                                                </Suspense>
                                            </Layout>
                                        ) : (
                                            <Suspense fallback={<Loader />}>
                                                <Component />
                                            </Suspense>
                                        )
                                    }
                                />
                            );
                        });
                    });
                })}
            </Routes>
        </>
    );
}
