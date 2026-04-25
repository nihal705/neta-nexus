import { useState, useEffect } from 'react';
import axios from 'axios';

const PARTY_SYMBOLS_CACHE = {};

export default function PartySymbol({ partyName, size = "md", showName = false }) {
    const [symbol, setSymbol] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchPartySymbol();
    }, [partyName]);

    const fetchPartySymbol = async () => {
        if (PARTY_SYMBOLS_CACHE[partyName]) {
            setSymbol(PARTY_SYMBOLS_CACHE[partyName]);
            setLoading(false);
            return;
        }

        try {
            const response = await axios.get(`http://localhost:8000/api/parties/symbol/${encodeURIComponent(partyName)}`);
            PARTY_SYMBOLS_CACHE[partyName] = response.data;
            setSymbol(response.data);
        } catch (error) {
            console.error('Error fetching party symbol:', error);
            setSymbol({ symbol: "🏛️", color: "#666666", short_name: partyName?.slice(0, 15) });
        } finally {
            setLoading(false);
        }
    };

    const sizeClasses = {
        sm: "text-lg",
        md: "text-2xl",
        lg: "text-4xl",
        xl: "text-6xl"
    };

    if (loading) {
        return <div className={`${sizeClasses[size]} animate-pulse bg-gray-200 rounded-full w-8 h-8`}></div>;
    }

    return (
        <div className="flex items-center gap-2">
            <div 
                className={`flex items-center justify-center rounded-full ${size === 'sm' ? 'w-6 h-6' : size === 'md' ? 'w-8 h-8' : size === 'lg' ? 'w-12 h-12' : 'w-16 h-16'} bg-opacity-10`}
                style={{ backgroundColor: `${symbol?.color}20` }}
            >
                <span className={sizeClasses[size]}>{symbol?.symbol || "🏛️"}</span>
            </div>
            {showName && (
                <span className="text-sm font-medium" style={{ color: symbol?.color }}>
                    {symbol?.short_name || partyName}
                </span>
            )}
        </div>
    );
}