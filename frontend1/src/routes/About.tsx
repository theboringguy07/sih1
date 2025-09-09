import React from 'react'
import { motion } from 'framer-motion'
import { Shield, Target, Users, Eye } from 'lucide-react'

const Section: React.FC<{ title: string; text: string }> = ({ title, text }) => (
  <div className="about-card">
    <h3 className="about-title">{title}</h3>
    <p className="about-text">{text}</p>
  </div>
)

const About: React.FC = () => {
  return (
    <div className="py-20 transition-colors duration-300">
      <div className="max-w-6xl mx-auto px-6">
        <h1 className="text-4xl md:text-5xl font-bold tracking-tight text-center mb-4 bg-gradient-to-r from-indigo-500 to-purple-600 bg-clip-text text-transparent">About</h1>
        <p className="text-center max-w-3xl mx-auto mb-12 text-gray-400 dark:text-gray-300">A modern, AI-assisted platform helping students and young professionals discover meaningful internships faster.</p>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {[
            {t: 'Mission', d: 'Connect youth across India with relevant internships and career opportunities.', Icon: Target},
            {t: 'Who Can Apply', d: 'Students and early-career professionals from diverse fields and education levels.', Icon: Users},
            {t: 'How It Helps', d: 'AI-powered matching plus profile inputs yields better-fit recommendations and higher response rates.', Icon: Shield},
            {t: 'Vision', d: 'Equal access to opportunities, enabling growth and skill development for everyone.', Icon: Eye},
            {t: 'Privacy', d: 'Data is processed securely and used solely to personalize your recommendations.', Icon: Shield},
          ].map(({ t, d, Icon }, idx) => (
            <motion.div
              key={t}
              initial={{ opacity: 0, y: 12, scale: 0.98 }}
              whileInView={{ opacity: 1, y: 0, scale: 1 }}
              viewport={{ once: true, amount: 0.3 }}
              transition={{ duration: 0.4, delay: idx * 0.05 }}
              className="rounded-2xl p-8 shadow-xl hover:shadow-2xl hover:scale-[1.02] transition-all duration-300 bg-white/90 dark:bg-slate-800/90 border border-slate-200/60 dark:border-white/10"
            >
              <div className="w-10 h-10 rounded-full bg-gradient-to-r from-indigo-500 to-purple-600 flex items-center justify-center mb-4">
                <Icon className="w-5 h-5 text-white" />
              </div>
              <h3 className="text-xl font-semibold mb-2 text-slate-900 dark:text-white">{t}</h3>
              <p className="text-slate-700 dark:text-slate-300 leading-relaxed">{d}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default About


