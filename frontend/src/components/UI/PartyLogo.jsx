import { useState, useEffect } from 'react';

// Real party logos mapping
const PARTY_LOGOS = {
    'Bharatiya Janata Party': '/static/party_logos/Bharatiya_Janata_Party.png',
    'Indian National Congress': '/static/party_logos/Indian_National_Congress.png',
    'Aam Aadmi Party': '/static/party_logos/Aam_Aadmi_Party.png',
    'All India Trinamool Congress': '/static/party_logos/All_India_Trinamool_Congress.png',
    'Samajwadi Party': '/static/party_logos/Samajwadi_Party.png',
    'Bahujan Samaj Party': '/static/party_logos/Bahujan_Samaj_Party.png',
    'Communist Party of India (Marxist)': '/static/party_logos/Communist_Party_of_India_Marxist.png',
};

export default function PartyLogo({ partyName, size = "md", showName = false }) {
    const [imageError, setImageError] = useState(false);
    
    const logoPath = PARTY_LOGOS[partyName];
    const sizeClasses = {
        sm: "w-6 h-6",
        md: "w-8 h-8",
        lg: "w-12 h-12",
        xl: "w-16 h-16"
    };
    
    if (!logoPath || imageError) {
        return (
            <div className={`${sizeClasses[size]} rounded-full bg-gray-200 flex items-center justify-center`}>
                <span className="text-xs text-gray-500">{partyName?.charAt(0) || '?'}</span>
            </div>
        );
    }
    
    return (
        <img 
            src={logoPath}
            alt={partyName}
            className={`${sizeClasses[size]} rounded-full object-cover`}
            onError={() => setImageError(true)}
        />
    );
}