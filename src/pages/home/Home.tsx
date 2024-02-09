import React, { useState } from 'react';
import './Home.css';
import { IPhaseItem } from '../../components/phase_item/PhaseItem';
import PhaseList from '../../components/phase_list/PhaseList';
import Player from '../../components/player/Player';
import defaultPhaseItems from '../../data/default_phase_items.json';

export default function Home() {
    const [phaseItems, setPhaseItems] = useState(defaultPhaseItems);

    function removePhaseItem(index: number) {
        const newPhaseItems = phaseItems.filter((_: any, i: number) => i !== index);
        setPhaseItems(newPhaseItems);
    }

    function addPhaseItem(item: IPhaseItem) {
        const newPhaseItems = [...phaseItems, item];
        setPhaseItems(newPhaseItems);
    }

    return (
        <div className="App">
            <Player />
            <PhaseList phase_items={phaseItems} />
        </div>
    );
}
