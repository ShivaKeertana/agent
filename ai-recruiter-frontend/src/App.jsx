import React, { useState } from 'react';
import axios from 'axios';
import { MessageCircle, User, Briefcase, Star, AlertTriangle, Loader2, X } from 'lucide-react';

function App() {
  const [jobDesc, setJobDesc] = useState('We are looking for a fast-paced React Developer with 3+ years experience. Node.js is a plus.');
  const [resumeLinks, setResumeLinks] = useState('https://linkedin.com/in/candidate1\nhttps://github.com/candidate2');
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [chatModalCandidate, setChatModalCandidate] = useState(null);

  const handleProcess = async () => {
    setLoading(true);
    try {
      const linksArray = resumeLinks.split('\n').filter(link => link.trim() !== '');
      // Make sure this URL matches your backend!
      const response = await axios.post('http://localhost:8000/api/process-recruitment', {
        job_description: jobDesc,
        resume_links: linksArray
      });
      setData(response.data);
    } catch (error) {
      console.error("Error processing:", error);
      alert("Failed to process data. Is the backend running?");
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8 font-sans">
      <div className="max-w-7xl mx-auto space-y-8">
        
        {/* Header & Inputs */}
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <h1 className="text-3xl font-bold text-gray-800 mb-6 flex items-center gap-2">
            <Briefcase className="text-blue-600" /> AI Recruiter Agent
          </h1>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Job Description</label>
              <textarea 
                className="w-full p-3 border rounded-lg h-32 focus:ring-2 focus:ring-blue-500 outline-none"
                value={jobDesc}
                onChange={(e) => setJobDesc(e.target.value)}
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Resume Links (One per line)</label>
              <textarea 
                className="w-full p-3 border rounded-lg h-32 focus:ring-2 focus:ring-blue-500 outline-none"
                value={resumeLinks}
                onChange={(e) => setResumeLinks(e.target.value)}
              />
            </div>
          </div>
          <button 
            onClick={handleProcess}
            disabled={loading}
            className="mt-6 bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-8 rounded-lg flex items-center gap-2 disabled:bg-blue-300 transition-colors"
          >
            {loading ? <Loader2 className="animate-spin" /> : <Star />}
            {loading ? 'AI is analyzing & chatting...' : 'Discover & Screen Candidates'}
          </button>
        </div>

        {/* Results Section */}
        {data && (
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
            
            {/* A. JD Parsing Side Panel (Card) */}
            <div className="lg:col-span-1 bg-blue-50 border border-blue-100 p-6 rounded-xl h-fit">
              <h3 className="text-lg font-bold text-blue-900 mb-4 border-b border-blue-200 pb-2">JD Analysis</h3>
              <div className="space-y-4 text-sm">
                <div>
                  <span className="font-semibold text-blue-800">Role Type:</span>
                  <p className="text-gray-700">{data.jd_summary.role_type}</p>
                </div>
                <div>
                  <span className="font-semibold text-blue-800">Experience:</span>
                  <p className="text-gray-700">{data.jd_summary.experience_level}</p>
                </div>
                <div>
                  <span className="font-semibold text-blue-800">Required Skills:</span>
                  <div className="flex flex-wrap gap-1 mt-1">
                    {data.jd_summary.required_skills.map((s, i) => (
                      <span key={i} className="bg-blue-200 text-blue-800 px-2 py-0.5 rounded text-xs">{s}</span>
                    ))}
                  </div>
                </div>
                <div>
                  <span className="font-semibold text-purple-800">Hidden Expectations:</span>
                  <p className="text-gray-700 italic">{data.jd_summary.hidden_expectations}</p>
                </div>
              </div>
            </div>

            {/* B, D, E. Main Unified Table */}
            <div className="lg:col-span-3 bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse">
                  <thead>
                    <tr className="bg-gray-100 text-gray-600 text-sm uppercase tracking-wider">
                      <th className="p-4 font-semibold">Candidate</th>
                      <th className="p-4 font-semibold">Match %</th>
                      <th className="p-4 font-semibold">Interest</th>
                      <th className="p-4 font-semibold">Final Score</th>
                      <th className="p-4 font-semibold">Status</th>
                      <th className="p-4 font-semibold">Action</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-100">
                    {data.candidates.map((cand, idx) => (
                      <tr key={cand.id} className="hover:bg-gray-50 transition-colors">
                        <td className="p-4">
                          <div className="font-bold text-gray-800 flex items-center gap-2">
                            <span className="text-gray-400">#{idx + 1}</span> {cand.name}
                          </div>
                          {cand.missing_skills.length > 0 && (
                            <div className="text-xs text-red-500 mt-1">
                              Missing: {cand.missing_skills.join(', ')}
                            </div>
                          )}
                        </td>
                        <td className="p-4 font-medium text-gray-700">{cand.match_score}%</td>
                        <td className="p-4">
                          <span className={`px-2 py-1 rounded-full text-xs font-bold ${
                            cand.interest_level === 'High' ? 'bg-green-100 text-green-700' :
                            cand.interest_level === 'Medium' ? 'bg-yellow-100 text-yellow-700' :
                            'bg-red-100 text-red-700'
                          }`}>
                            {cand.interest_level}
                          </span>
                        </td>
                        <td className="p-4 font-black text-lg text-blue-900">{cand.final_score}</td>
                        <td className="p-4 font-medium">
                          {cand.status.includes('⭐') ? 
                            <span className="text-amber-500 flex items-center gap-1"><Star size={16}/> Recommended</span> : 
                            <span className="text-red-500 flex items-center gap-1"><AlertTriangle size={16}/> Risk</span>
                          }
                        </td>
                        <td className="p-4">
                          <button 
                            onClick={() => setChatModalCandidate(cand)}
                            className="text-blue-600 hover:text-blue-800 flex items-center gap-1 font-semibold text-sm border border-blue-200 px-3 py-1.5 rounded-lg hover:bg-blue-50 transition-colors"
                          >
                            <MessageCircle size={16} /> View Chat
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* C. AI Engagement Chat Modal */}
        {chatModalCandidate && (
          <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50 p-4">
            <div className="bg-white w-full max-w-lg rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[80vh]">
              {/* Modal Header */}
              <div className="bg-blue-600 p-4 flex justify-between items-center text-white">
                <div>
                  <h3 className="font-bold text-lg">AI Outreach Log</h3>
                  <p className="text-blue-100 text-sm">Simulated conversation with {chatModalCandidate.name}</p>
                </div>
                <button onClick={() => setChatModalCandidate(null)} className="hover:bg-blue-700 p-1 rounded-full">
                  <X size={24} />
                </button>
              </div>
              
              {/* Chat View */}
              <div className="p-6 flex-1 overflow-y-auto space-y-4 bg-gray-50">
                {chatModalCandidate.chat_log.map((chat, idx) => (
                  <div key={idx} className={`flex ${chat.role === 'AI' ? 'justify-start' : 'justify-end'}`}>
                    <div className={`max-w-[80%] p-3 rounded-2xl ${
                      chat.role === 'AI' ? 'bg-white border border-gray-200 text-gray-800 rounded-tl-none shadow-sm' 
                      : 'bg-blue-600 text-white rounded-tr-none shadow-md'
                    }`}>
                      <div className="text-xs font-bold mb-1 opacity-70 flex items-center gap-1">
                        {chat.role === 'AI' ? <Star size={12}/> : <User size={12}/>}
                        {chat.role}
                      </div>
                      <div className="text-sm">{chat.message}</div>
                    </div>
                  </div>
                ))}
              </div>

              {/* Interest Engine Reason Footer */}
              <div className="bg-gray-100 p-4 border-t border-gray-200">
                <span className="text-xs font-bold uppercase text-gray-500">AI Interest Analysis</span>
                <p className="text-sm text-gray-800 mt-1">{chatModalCandidate.reason}</p>
              </div>
            </div>
          </div>
        )}

      </div>
    </div>
  );
}

export default App;