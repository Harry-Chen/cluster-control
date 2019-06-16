import React from 'react';

import Typography from '@material-ui/core/Typography';
import Slider from '@material-ui/lab/Slider';

import './App.css';

interface ClusterControl {
    fanLevel: number;
    cpuFrequencyAvg: number;
    cpuFrequencyMax: number;
    gpuPower: number;
    gpuFrequency: number;
}

interface EnableControl {
    notice: string;
    enabled: boolean;
}

type AppState = ClusterControl & EnableControl;

const initialState: AppState = {
    fanLevel: 0,
    cpuFrequencyAvg: 205,
    cpuFrequencyMax: 255,
    gpuPower: 250,
    gpuFrequency: 1380,
    enabled: false,
    notice: 'Fetching current state...'
};

// const SERVER_URL = 'http://mon.sc.team:9000';
const SERVER_URL = 'http://localhost:3000';
const SERVER_STATE_URL = SERVER_URL + '/control';

const App: React.FC = () => {

    const [state, setState] = React.useState<AppState>(initialState);

    // component did mount
    React.useEffect(() => {
        fetch(SERVER_STATE_URL)
            .then(r => r.json())
            .then((r: ClusterControl) => {
                setState({
                    ...r,
                    notice: 'State successfully fetched!',
                    enabled: true
                });
            })
            .catch(e => {
                setState({
                    ...state,
                    notice: 'Failed to fetch state, please refresh!',
                    enabled: false
                });
            })
    }, []);


    const stateChange = () => {

        // disable changing
        setState({
            ...state,
            notice: 'Sending new state to server...',
            enabled: false
        });

        fetch(SERVER_STATE_URL, {
            body: JSON.stringify(state),
            method: 'POST'
        })
            .then(r => r.json())
            .then((r: ClusterControl) => {
                setState({
                    ...r,
                    notice: 'State successfully changed!',
                    enabled: true,
                });
            })
            .catch(e => {
                setState({
                    ...state,
                    notice: 'Failed to change state, please refresh!',
                    enabled: false
                });
            })
    };

    return (
        <div className="App">
            <Typography variant="h4" className="title" gutterBottom>
                {state.notice}
            </Typography>
            <div className='sliders'>
            <div className="slider">
                <Typography className="slider-title" gutterBottom>
                    Fan
                </Typography>
                <Slider
                    className="slider-content"
                    orientation="vertical"
                    defaultValue={initialState.fanLevel}
                    value={state.fanLevel}
                    min={0}
                    max={100}
                    step={1}
                    disabled={!state.enabled}
                    valueLabelDisplay="on"
                    onChange={(e, n) => {
                        setState({
                            ...state,
                            fanLevel: n as number
                        })
                    }}
                    onMouseUp={stateChange}
                    onTouchEnd={stateChange}
                />
            </div>
            <div className="slider">
                <Typography className="slider-title" gutterBottom>
                    CPU Power
                </Typography>
                <Slider
                    className="slider-content"
                    orientation="vertical"
                    defaultValue={[initialState.cpuFrequencyAvg, initialState.cpuFrequencyMax]}
                    value={[state.cpuFrequencyAvg, state.cpuFrequencyMax]}
                    min={1}
                    max={255}
                    step={0.5}
                    disabled={!state.enabled}
                    valueLabelDisplay="on"
                    onChange={(e, n) => {
                        const numbers = (n as number[]).sort();
                        setState({
                            ...state,
                            cpuFrequencyAvg: numbers[0],
                            cpuFrequencyMax: numbers[1],
                        })
                    }}
                    onMouseUp={stateChange}
                    onTouchEnd={stateChange}
                />
            </div>
            <div className="slider">
                <Typography className="slider-title" gutterBottom>
                    GPU Power
                </Typography>
                <Slider
                    className="slider-content"
                    orientation="vertical"
                    defaultValue={initialState.gpuPower}
                    value={state.gpuPower}
                    min={100}
                    max={250}
                    disabled={!state.enabled}
                    valueLabelDisplay="on"
                    onChange={(e, n) => {
                        setState({
                            ...state,
                            gpuPower: n as number,
                        })
                    }}
                    onMouseUp={stateChange}
                    onTouchEnd={stateChange}
                />
            </div>
            <div className="slider">
                <Typography className="slider-title" gutterBottom>
                    GPU Frequency
                </Typography>
                <Slider
                    className="slider-content"
                    orientation="vertical"
                    defaultValue={initialState.gpuFrequency}
                    value={state.gpuFrequency}
                    min={135}
                    max={1350}
                    step={7.5}
                    disabled={!state.enabled}
                    valueLabelDisplay="on"
                    onChange={(e, n) => {
                        setState({
                            ...state,
                            gpuFrequency: n as number,
                        })
                    }}
                    onMouseUp={stateChange}
                    onTouchEnd={stateChange}
                />
            </div>
            </div>
        </div>
    );
};

export default App;
