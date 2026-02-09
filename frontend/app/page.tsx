'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { signInApi, signUpApi } from '@/lib/auth';

export default function Home() {
  const [isSignUp, setIsSignUp] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      if (isSignUp) {
        await signUpApi(email, password, name);
      } else {
        await signInApi(email, password);
      }
      router.push('/dashboard');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Authentication failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#020202] text-white flex overflow-hidden font-sans">
      
      {/* LEFT SIDE: Visual/Branding (Hidden on Mobile) */}
      <div className="hidden lg:flex lg:w-1/2 relative flex-col justify-center px-12 overflow-hidden border-r border-white/5">
        <div className="absolute top-0 left-0 w-full h-full bg-[radial-gradient(circle_at_20%_30%,rgba(79,70,229,0.15),transparent_50%)]"></div>
        <div className="relative z-10 space-y-6">
          <div className="w-12 h-12 bg-indigo-500 rounded-2xl flex items-center justify-center shadow-[0_0_30px_rgba(99,102,241,0.4)]">
             <svg className="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
             </svg>
          </div>
          <h2 className="text-6xl font-black tracking-tighter leading-tight">
            Manage tasks <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-cyan-400">
              with precision.
            </span>
          </h2>
          <p className="text-slate-400 text-lg max-w-md font-light leading-relaxed">
            The minimal, high-performance task manager for developers who want to stay focused and organized.
          </p>
          <div className="flex gap-4 pt-4">
            <div className="px-4 py-2 bg-white/5 border border-white/10 rounded-full text-xs text-slate-300">✦ Fast Deployment</div>
            <div className="px-4 py-2 bg-white/5 border border-white/10 rounded-full text-xs text-slate-300">✦ End-to-End Encryption</div>
          </div>
        </div>
      </div>

      {/* RIGHT SIDE: Auth Form */}
      <div className="w-full lg:w-1/2 flex items-center justify-center p-8 relative">
        {/* Decorative Blur for Mobile */}
        <div className="lg:hidden absolute top-0 left-1/2 -translate-x-1/2 w-64 h-64 bg-indigo-500/20 blur-[100px]"></div>

        <div className="w-full max-w-sm space-y-8 relative z-10">
          <div className="space-y-2">
            <h3 className="text-3xl font-bold tracking-tight">
              {isSignUp ? 'Create an account' : 'Welcome back'}
            </h3>
            <p className="text-slate-500 text-sm font-medium">
              Enter your credentials to access your dashboard.
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            {isSignUp && (
              <div className="space-y-1">
                <input
                  type="text"
                  placeholder="Full Name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="w-full px-5 py-4 bg-[#0A0A0A] border border-white/10 rounded-2xl focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/50 transition-all outline-none text-sm"
                />
              </div>
            )}

            <div className="space-y-1">
              <input
                type="email"
                placeholder="Email Address"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="w-full px-5 py-4 bg-[#0A0A0A] border border-white/10 rounded-2xl focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/50 transition-all outline-none text-sm"
              />
            </div>

            <div className="space-y-1">
              <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="w-full px-5 py-4 bg-[#0A0A0A] border border-white/10 rounded-2xl focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/50 transition-all outline-none text-sm"
              />
            </div>

            {error && (
              <p className="text-red-400 text-xs px-2 animate-pulse">{error}</p>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full py-4 bg-white text-black font-bold rounded-2xl hover:bg-slate-200 transition-all active:scale-95 disabled:opacity-50 mt-4 flex items-center justify-center gap-2"
            >
              {loading ? 'Processing...' : (isSignUp ? 'Sign Up Free' : 'Sign In')}
            </button>
          </form>

          <div className="relative py-4">
            <div className="absolute inset-0 flex items-center"><div className="w-full border-t border-white/5"></div></div>
            <div className="relative flex justify-center text-xs uppercase"><span className="bg-[#020202] px-2 text-slate-500">Or continue with</span></div>
          </div>

          <button
            onClick={() => setIsSignUp(!isSignUp)}
            className="w-full py-3 bg-transparent border border-white/10 text-white rounded-2xl text-sm font-medium hover:bg-white/5 transition-colors"
          >
            {isSignUp ? 'Already have an account? Log in' : "Don't have an account? Sign up"}
          </button>

          <p className="text-center text-[10px] text-slate-600 uppercase tracking-widest leading-loose">
            Security Guaranteed • ISO 27001 Certified
          </p>
        </div>
      </div>
    </div>
  );
}