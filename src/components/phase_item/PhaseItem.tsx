import React, { useState } from 'react'
import "./PhaseItem.css"

export interface IPhaseItem {
    name: string,
    thumbnail_path: string,
    audio_path: string
}

export default function PhaseItem(props: IPhaseItem) {
    const [imgSrc, setImgSrc] = useState(props.thumbnail_path);
    const defaultThumbnail = 'logo192.png';

    const handlePlay = () => {
        console.log("Playing", props.audio_path);
    };

    const handleError = () => {
        setImgSrc(defaultThumbnail);
    };

    return (
        <div className="phase-item">
            <img src={imgSrc} alt={props.name} onError={handleError} className="thumbnail" />
            <div className="phase-name">{props.name}</div>
            <button className="play-button" onClick={handlePlay}>Play</button>
        </div>
    );
}
