"use client";

export function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="border-t border-slate-200/50 dark:border-slate-700/50 bg-white/50 dark:bg-slate-900/50 backdrop-blur-xl">
      <div className="container max-w-7xl px-4 py-12">
        <div className="grid md:grid-cols-4 gap-8 mb-8">
          {/* Brand */}
          <div>
            <h3 className="text-lg font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-2">
              AI Agent System
            </h3>
            <p className="text-sm text-slate-600 dark:text-slate-400">
              Build, manage, and deploy intelligent AI agents that collaborate.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="font-semibold text-slate-900 dark:text-white mb-4">Product</h4>
            <ul className="space-y-2 text-sm text-slate-600 dark:text-slate-400">
              <li><a href="/" className="hover:text-slate-900 dark:hover:text-white transition-colors">Home</a></li>
              <li><a href="/playground" className="hover:text-slate-900 dark:hover:text-white transition-colors">Playground</a></li>
              <li><a href="/agents" className="hover:text-slate-900 dark:hover:text-white transition-colors">Agents</a></li>
            </ul>
          </div>

          {/* Resources */}
          <div>
            <h4 className="font-semibold text-slate-900 dark:text-white mb-4">Resources</h4>
            <ul className="space-y-2 text-sm text-slate-600 dark:text-slate-400">
              <li><a href="#" className="hover:text-slate-900 dark:hover:text-white transition-colors">Documentation</a></li>
              <li><a href="#" className="hover:text-slate-900 dark:hover:text-white transition-colors">API Reference</a></li>
              <li><a href="#" className="hover:text-slate-900 dark:hover:text-white transition-colors">GitHub</a></li>
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h4 className="font-semibold text-slate-900 dark:text-white mb-4">Connect</h4>
            <ul className="space-y-2 text-sm text-slate-600 dark:text-slate-400">
              <li><a href="#" className="hover:text-slate-900 dark:hover:text-white transition-colors">Twitter</a></li>
              <li><a href="#" className="hover:text-slate-900 dark:hover:text-white transition-colors">LinkedIn</a></li>
              <li><a href="#" className="hover:text-slate-900 dark:hover:text-white transition-colors">Discord</a></li>
            </ul>
          </div>
        </div>

        {/* Divider */}
        <div className="h-px bg-gradient-to-r from-transparent via-slate-300 dark:via-slate-700 to-transparent mb-8" />

        {/* Bottom */}
        <div className="flex flex-col md:flex-row justify-between items-center text-sm text-slate-600 dark:text-slate-400">
          <p>&copy; {currentYear} AI Agent System. All rights reserved.</p>
          <div className="flex gap-6 mt-4 md:mt-0">
            <a href="#" className="hover:text-slate-900 dark:hover:text-white transition-colors">Privacy Policy</a>
            <a href="#" className="hover:text-slate-900 dark:hover:text-white transition-colors">Terms of Service</a>
          </div>
        </div>
      </div>
    </footer>
  );
}
