export default function Page() {
    return (
        <iframe
            src="http://localhost:8888"
            style={{ width: '100%', height: '100vh', border: 'none' }}
            title="Embedded Page"
            sandbox="allow-popups allow-scripts allow-forms allow-same-origin"
        ></iframe>
    );
}
