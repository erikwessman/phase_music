import React, { useState } from 'react'
import "./Player.css"

export default function Player() {
    const [playState, setPlayState] = useState("Paused");
    const [currentTime, setCurrentTime] = useState(0)
    const [duration, setDuration] = useState(300)

    function formatTime(seconds: number) {
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = Math.floor(seconds % 60);
        return `${minutes}:${remainingSeconds < 10 ? '0' : ''}${remainingSeconds}`;
    };

    function togglePlay() {
        setPlayState(playState === "Playing" ? "Paused" : "Playing");
    };

    function fastForward() {
        console.log("Fast forwarded 15 seconds");
    };

    function rewind() {
        console.log("Rewinded 15 seconds");
    };

    return (
        <div className="player-container">
            <button className="player-button" onClick={rewind}>Rewind 15s</button>
            <button className="player-button" onClick={togglePlay}>
                {playState === "Playing" ? "Pause" : "Play"}
            </button>
            <button className="player-button" onClick={fastForward}>Fast Forward 15s</button>

            <div className="progress-container">
                <span className="time">{formatTime(currentTime)}</span>
                <span>/</span>
                <span className="time">{formatTime(duration)}</span>
            </div>
        </div>
    );
}
