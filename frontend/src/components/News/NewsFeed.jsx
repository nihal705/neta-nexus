import { useState, useEffect } from 'react';
import axios from 'axios';
import { FiExternalLink, FiClock } from 'react-icons/fi';

export default function NewsFeed({ candidateName }) {
    const [articles, setArticles] = useState([]);
    const [loading, setLoading] = useState(true);
    
    useEffect(() => {
        fetchNews();
    }, [candidateName]);
    
    const fetchNews = async () => {
        try {
            const response = await axios.get(`/api/news/trending`);
            setArticles(response.data.articles || []);
        } catch (error) {
            console.error('Error fetching news:', error);
        } finally {
            setLoading(false);
        }
    };
    
    if (loading) return <div className="text-center py-8">Loading news...</div>;
    
    return (
        <div>
            <h3 className="text-xl font-semibold mb-4">Latest Political News</h3>
            <div className="space-y-4">
                {articles.map((article, idx) => (
                    <a
                        key={idx}
                        href={article.link}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="block p-4 border border-gray-200 rounded-lg hover:shadow-md transition group"
                    >
                        <div className="flex justify-between items-start">
                            <div className="flex-1">
                                <h4 className="font-semibold group-hover:text-primary-teal transition">
                                    {article.title}
                                </h4>
                                {article.description && (
                                    <p className="text-sm text-gray-500 mt-1">{article.description}</p>
                                )}
                                <div className="flex items-center gap-4 mt-2 text-xs text-gray-400">
                                    <span className="flex items-center gap-1">
                                        <FiClock size={12} /> {new Date(article.pub_date).toLocaleDateString()}
                                    </span>
                                    <span>{article.source}</span>
                                </div>
                            </div>
                            <FiExternalLink className="text-gray-400 group-hover:text-primary-teal ml-2" />
                        </div>
                    </a>
                ))}
            </div>
            {articles.length === 0 && (
                <p className="text-center text-gray-500 py-8">No recent news found</p>
            )}
        </div>
    );
}