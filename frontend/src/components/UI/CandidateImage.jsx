import { useState } from 'react';

export default function CandidateImage({ candidateId, name, size = "md", partyColor }) {
    const [imageError, setImageError] = useState(false);
    
    const sizeClasses = {
        sm: "w-8 h-8 text-xs",
        md: "w-12 h-12 text-sm",
        lg: "w-16 h-16 text-base",
        xl: "w-24 h-24 text-xl"
    };
    
    const imageUrl = `/static/candidate_photos/${candidateId}.jpg`;
    
    if (imageError) {
        // Generate avatar from name
        const initials = name.split(' ').map(n => n[0]).join('').slice(0, 2).toUpperCase();
        
        return (
            <div 
                className={`${sizeClasses[size]} rounded-full flex items-center justify-center font-bold text-white`}
                style={{ backgroundColor: partyColor || '#00A896' }}
            >
                {initials || '?'}
            </div>
        );
    }
    
    return (
        <img
            src={imageUrl}
            alt={name}
            className={`${sizeClasses[size]} rounded-full object-cover`}
            onError={() => setImageError(true)}
        />
    );
}