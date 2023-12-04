import logo from './logo.svg';
import './App.css';

// WebcamCapture.js
import React, { useRef, useCallback, useEffect, useState } from 'react';
import Webcam from 'react-webcam';


const WebcamCapture = () => {
  const webcamRef = useRef(null);
  const timerRef = useRef(null);

  const capture = useCallback(() => {
    const imageSrc = webcamRef.current.getScreenshot();

    if (imageSrc) {
      sendRequest(imageSrc)
    }
  }, [webcamRef]);


  const [isRecording, setIsRecording] = useState(false)

  const [output, setResponseOutput] = useState("")




  const startRecording = function() {
    if (timerRef.current) {
      clearInterval(timerRef.current);
    }

    timerRef.current = setInterval(capture, 5000);
  }


  useEffect(() => {
    return () => {
      clearInterval(timerRef.current);
    };
  }, []);


  const sendRequest = async (imgs) => {
    if (imgs) {
      try {
        const response = await fetch('http://127.0.0.1:8004/upload', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ image: imgs }),
        });
        
        const resp = await response.json()

        if (resp.data) {
          setResponseOutput(resp.data)
        }
        
        
      } catch (error) {
        console.error('Error sending the request:', error);
      }
    }
  };

  useEffect(() => {
    if (isRecording) {
      startRecording()
    } else {
      clearInterval(timerRef.current)
    }
  }, [isRecording])


  const action =  () => {
    setIsRecording(isRecording => !isRecording)
  };

  return (
    <div>
      <Webcam
        audio={false}
        height={720}
        ref={webcamRef}
        screenshotFormat="image/jpeg"
        width={1280}
      />
      
      <button onClick={action}>{ !isRecording ? 'Start Recording' : 'Stop Recording'}</button>

      <br></br>

      <b>{output}</b>
    </div>
  );
};


function App() {
  return (
    <div className="App">
      <WebcamCapture />
    </div>
  );
}

export default App;
