import React from 'react'
import PhaseItem, { IPhaseItem } from '../phase_item/PhaseItem'
import "./PhaseList.css"

export default function PhaseList(props: { phase_items: IPhaseItem[] }) {
    const handleRemove = (index: number) => {
    };

    return (
        <div className="phase-list-container">
            <ul>
                {props.phase_items.map((item, index) => (
                    <li key={index} className="phase-list-item">
                        <PhaseItem name={item.name} thumbnail_path={item.thumbnail_path} audio_path={item.audio_path} />
                        <button className="remove-button" onClick={() => handleRemove(index)}>×</button>
                    </li>
                ))}
            </ul>
        </div>
    );
}
