import { useState, useEffect } from 'react';
import axios from 'axios';

export default function CandidateAvatar({ candidate, size = "md" }) {
    const [imageData, setImageData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchCandidateImage();
    }, [candidate.id]);

    const fetchCandidateImage = async () => {
        try {
            const response = await axios.get(`http://localhost:8000/api/parties/candidate/${candidate.id}/image`);
            setImageData(response.data);
        } catch (error) {
            console.error('Error fetching candidate image:', error);
        } finally {
            setLoading(false);
        }
    };

    const sizeClasses = {
        sm: "w-8 h-8 text-sm",
        md: "w-12 h-12 text-base",
        lg: "w-16 h-16 text-xl",
        xl: "w-24 h-24 text-2xl"
    };

    if (loading) {
        return <div className={`${sizeClasses[size]} bg-gray-200 rounded-full animate-pulse`}></div>;
    }

    if (imageData?.has_image) {
        return (
            <img 
                src={imageData.url} 
                alt={candidate.name}
                className={`${sizeClasses[size]} rounded-full object-cover`}
                loading="lazy"
            />
        );
    }

    // Fallback to initials avatar
    return (
        <div 
            className={`${sizeClasses[size]} rounded-full flex items-center justify-center font-bold text-white`}
            style={{ backgroundColor: imageData?.color || "#00A896" }}
        >
            {imageData?.initials || candidate.name?.charAt(0) || "?"}
        </div>
    );
}