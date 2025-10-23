import { useState, useEffect } from 'react';
import { Play, Pause, Square } from 'lucide-react';
import { focusAPI } from '../services/api';

export default function Timer({ onSessionComplete }) {
  const [isActive, setIsActive] = useState(false);
  const [timeRemaining, setTimeRemaining] = useState(0);
  const [duration, setDuration] = useState(0);
  const [selectedDuration, setSelectedDuration] = useState(25);

  const durations = [
    { label: 'Pomodoro', value: 25, mode: 'pomodoro' },
    { label: 'Quick', value: 15, mode: 'quick' },
    { label: 'Deep Work', value: 90, mode: 'deepwork' },
  ];

  useEffect(() => {
    let interval;
    if (isActive) {
      interval = setInterval(async () => {
        try {
          const { data } = await focusAPI.getStatus();
          if (data.is_active) {
            setTimeRemaining(data.time_remaining);
            if (data.time_remaining <= 0) {
              handleStop(true);
            }
          }
        } catch (error) {
          console.error('Error fetching status:', error);
        }
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [isActive]);

  const handleStart = async (mins, mode) => {
    try {
      const { data } = await focusAPI.start(mins, mode);
      setIsActive(true);
      setDuration(mins * 60);
      setTimeRemaining(mins * 60);
      setSelectedDuration(mins);
    } catch (error) {
      console.error('Error starting session:', error);
      alert('Failed to start session. Make sure backend is running.');
    }
  };

  const handleStop = async (completed = false) => {
    try {
      await focusAPI.stop(completed);
      setIsActive(false);
      setTimeRemaining(0);
      if (completed && onSessionComplete) {
        onSessionComplete();
      }
    } catch (error) {
      console.error('Error stopping session:', error);
    }
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const progress = duration > 0 ? ((duration - timeRemaining) / duration) * 100 : 0;

  return (
    <div className="bg-white rounded-2xl shadow-lg p-8">
      <h2 className="text-3xl font-bold text-gray-800 mb-6 text-center">
        Focus Timer
      </h2>

      {!isActive ? (
        <div className="space-y-6">
          <div className="grid grid-cols-3 gap-4">
            {durations.map((d) => (
              <button
                key={d.value}
                onClick={() => handleStart(d.value, d.mode)}
                className="px-6 py-4 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-xl hover:from-blue-600 hover:to-blue-700 transition-all shadow-md hover:shadow-lg font-semibold"
              >
                <div className="text-2xl font-bold">{d.value}</div>
                <div className="text-sm opacity-90">{d.label}</div>
              </button>
            ))}
          </div>

          <div className="text-center text-gray-500 text-sm">
            Select a duration to start focusing
          </div>
        </div>
      ) : (
        <div className="space-y-6">
          <div className="relative w-64 h-64 mx-auto">
            <svg className="transform -rotate-90 w-64 h-64">
              <circle
                cx="128"
                cy="128"
                r="120"
                stroke="#e5e7eb"
                strokeWidth="12"
                fill="none"
              />
              <circle
                cx="128"
                cy="128"
                r="120"
                stroke="#3b82f6"
                strokeWidth="12"
                fill="none"
                strokeDasharray={`${2 * Math.PI * 120}`}
                strokeDashoffset={`${2 * Math.PI * 120 * (1 - progress / 100)}`}
                className="transition-all duration-1000"
              />
            </svg>
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="text-center">
                <div className="text-5xl font-bold text-gray-800">
                  {formatTime(timeRemaining)}
                </div>
                <div className="text-gray-500 mt-2">
                  {Math.round(progress)}% Complete
                </div>
              </div>
            </div>
          </div>

          <div className="flex justify-center gap-4">
            <button
              onClick={() => handleStop(false)}
              className="px-8 py-3 bg-red-500 text-white rounded-xl hover:bg-red-600 transition-all shadow-md hover:shadow-lg font-semibold flex items-center gap-2"
            >
              <Square size={20} />
              Stop
            </button>
          </div>

          <div className="text-center text-gray-600 text-sm">
            🚫 Distracting websites are now blocked
          </div>
        </div>
      )}
    </div>
  );
}
