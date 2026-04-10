/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { motion } from "motion/react";
import { Terminal, CheckCircle2, AlertCircle, BookOpen, Rocket, Github, Cpu } from "lucide-react";

export default function App() {
  return (
    <div className="min-h-screen bg-[#0a0a0a] text-gray-100 font-sans selection:bg-blue-500/30">
      {/* Background Glow */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-[20%] -left-[10%] w-[70%] h-[70%] bg-blue-500/10 blur-[120px] rounded-full" />
        <div className="absolute -bottom-[20%] -right-[10%] w-[70%] h-[70%] bg-purple-500/10 blur-[120px] rounded-full" />
      </div>

      <div className="relative max-w-6xl mx-auto px-6 py-12">
        {/* Header */}
        <header className="mb-16">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex items-center gap-3 mb-4"
          >
            <div className="p-2 bg-blue-500/20 rounded-lg border border-blue-500/30">
              <Cpu className="w-6 h-6 text-blue-400" />
            </div>
            <span className="text-sm font-mono text-blue-400 tracking-wider uppercase">OpenEnv Specification</span>
          </motion.div>
          
          <motion.h1 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="text-5xl md:text-7xl font-bold tracking-tight mb-6 bg-gradient-to-r from-white via-white to-gray-500 bg-clip-text text-transparent"
          >
            SupportAgent <br />
            <span className="text-blue-400">Environment</span>
          </motion.h1>
          
          <motion.p 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="text-xl text-gray-400 max-w-2xl leading-relaxed"
          >
            A real-world customer support triage and response environment designed for training and evaluating frontier AI agents.
          </motion.p>
        </header>

        {/* Action Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-20">
          {[
            { icon: Terminal, title: "OpenEnv Spec", desc: "Full compliance with typed models and standard API endpoints.", color: "blue" },
            { icon: Rocket, title: "3 Real Tasks", desc: "Easy, Medium, and Hard tasks with deterministic agent graders.", color: "purple" },
            { icon: CheckCircle2, title: "Reward Shaping", desc: "Meaningful partial progress signals and trajectory-based rewards.", color: "emerald" }
          ].map((item, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.3 + i * 0.1 }}
              className="p-6 rounded-2xl bg-white/5 border border-white/10 hover:border-white/20 transition-all group"
            >
              <item.icon className={`w-8 h-8 mb-4 text-${item.color}-400 group-hover:scale-110 transition-transform`} />
              <h3 className="text-lg font-semibold mb-2">{item.title}</h3>
              <p className="text-gray-400 text-sm leading-relaxed">{item.desc}</p>
            </motion.div>
          ))}
        </div>

        {/* Tasks Section */}
        <section className="mb-20">
          <h2 className="text-2xl font-bold mb-8 flex items-center gap-2">
            <BookOpen className="w-6 h-6 text-blue-400" />
            Environment Tasks
          </h2>
          <div className="space-y-4">
            {[
              { name: "Password Reset", diff: "Easy", desc: "Categorize and respond to a simple account recovery request.", score: "1.0" },
              { name: "Billing Update", diff: "Medium", desc: "Guide a user through updating credit card info in the portal.", score: "0.8" },
              { name: "Complex Shipping", diff: "Hard", desc: "Handle refunds, tracking, and address updates in one ticket.", score: "0.5" }
            ].map((task, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.5 + i * 0.1 }}
                className="flex items-center justify-between p-5 rounded-xl bg-white/5 border border-white/10"
              >
                <div>
                  <div className="flex items-center gap-3 mb-1">
                    <span className="text-lg font-medium">{task.name}</span>
                    <span className={`text-[10px] px-2 py-0.5 rounded-full border ${
                      task.diff === 'Easy' ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400' :
                      task.diff === 'Medium' ? 'bg-amber-500/10 border-amber-500/30 text-amber-400' :
                      'bg-rose-500/10 border-rose-500/30 text-rose-400'
                    }`}>
                      {task.diff}
                    </span>
                  </div>
                  <p className="text-sm text-gray-500">{task.desc}</p>
                </div>
                <div className="text-right">
                  <div className="text-xs text-gray-500 mb-1 font-mono uppercase tracking-widest">Baseline</div>
                  <div className="text-xl font-mono text-blue-400">{task.score}</div>
                </div>
              </motion.div>
            ))}
          </div>
        </section>

        {/* Submission Instructions */}
        <section className="p-8 rounded-3xl bg-gradient-to-br from-blue-600/20 to-purple-600/20 border border-white/10">
          <div className="flex flex-col md:flex-row gap-8 items-center">
            <div className="flex-1">
              <h2 className="text-3xl font-bold mb-4">Ready to Submit?</h2>
              <p className="text-gray-400 mb-6">
                Your OpenEnv environment is fully implemented and ready for deployment to Hugging Face Spaces. 
                Follow the instructions in the README.md to finalize your submission.
              </p>
              <div className="flex flex-wrap gap-4">
                <button className="px-6 py-3 bg-white text-black font-semibold rounded-xl hover:bg-gray-200 transition-colors flex items-center gap-2">
                  <Rocket className="w-4 h-4" />
                  Deploy to HF
                </button>
                <button className="px-6 py-3 bg-white/10 text-white font-semibold rounded-xl hover:bg-white/20 transition-colors flex items-center gap-2 border border-white/10">
                  <Github className="w-4 h-4" />
                  View Source
                </button>
              </div>
            </div>
            <div className="w-full md:w-72 p-4 bg-black/40 rounded-2xl border border-white/10 font-mono text-xs">
              <div className="flex items-center gap-2 mb-3 text-gray-500">
                <div className="w-2 h-2 rounded-full bg-red-500" />
                <div className="w-2 h-2 rounded-full bg-yellow-500" />
                <div className="w-2 h-2 rounded-full bg-green-500" />
                <span className="ml-2">inference.py</span>
              </div>
              <div className="text-blue-400"># Run baseline</div>
              <div className="text-gray-300">python inference.py</div>
              <div className="mt-4 text-emerald-400"># Output:</div>
              <div className="text-gray-500">[START] task=reset ...</div>
              <div className="text-gray-500">[STEP] step=1 ...</div>
              <div className="text-gray-500">[END] success=true ...</div>
            </div>
          </div>
        </section>

        {/* Footer */}
        <footer className="mt-20 pt-8 border-t border-white/5 text-center text-gray-600 text-sm">
          Built for the OpenEnv Specification &bull; 2026
        </footer>
      </div>
    </div>
  );
}
