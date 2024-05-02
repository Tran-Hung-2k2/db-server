import logo from '../assets/images/favicon.ico';

function Footer() {
    return (
        <footer className="p-10 footer text-base-content border-t-2">
            <aside>
                <img className="h-12 w-12" src={logo} alt="logo" />
                <p>
                    2023 Coursera Inc. All rights reserved.
                    <br />
                    Establish since 2012
                </p>
            </aside>
            <nav>
                <header className="footer-title">Coursera</header>
                <a className="link link-hover">About</a>
                <a className="link link-hover">What We Offer</a>
                <a className="link link-hover">Leadership</a>
                <a className="link link-hover">Careers</a>
                <a className="link link-hover">Catalog</a>
                <a className="link link-hover">Coursera Plus</a>
                <a className="link link-hover">Professional Certificates</a>
                <a className="link link-hover">MasterTrack® Certificates</a>
                <a className="link link-hover">Degrees</a>
                <a className="link link-hover">For Enterprise</a>
                <a className="link link-hover">For Government</a>
                <a className="link link-hover">For Campus</a>
                <a className="link link-hover">Become a Partner</a>
                <a className="link link-hover">Coronavirus Response</a>
                <a className="link link-hover">Social Impact</a>
            </nav>
            <nav>
                <header className="footer-title">Community</header>
                <a className="link link-hover">Learners</a>
                <a className="link link-hover">Partners</a>
                <a className="link link-hover">Beta Testers</a>
                <a className="link link-hover">Translators</a>
                <a className="link link-hover">Blog</a>
                <a className="link link-hover">The Coursera Podcast</a>
                <a className="link link-hover">Tech Blog</a>
                <a className="link link-hover">Teaching Center</a>
            </nav>
            <nav>
                <header className="footer-title">More</header>
                <a className="link link-hover">Press</a>
                <a className="link link-hover">Investors</a>
                <a className="link link-hover">Terms</a>
                <a className="link link-hover">Privacy</a>
                <a className="link link-hover">Help</a>
                <a className="link link-hover">Accessibility</a>
                <a className="link link-hover">Contact</a>
                <a className="link link-hover">Articles</a>
                <a className="link link-hover">Directory</a>
                <a className="link link-hover">Affiliates</a>
                <a className="link link-hover">Modern Slavery Statement</a>
                <a className="link link-hover">Manage Cookie Preferences</a>
            </nav>
        </footer>
    );
}

export default Footer;
