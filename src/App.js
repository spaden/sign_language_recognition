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
        const response = await fetch('https://jsonplaceholder.typicode.com/todos/1', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
          //body: JSON.stringify({ image: imgs }),
        });
        
        //const resp = await response.json()

        const dt = ['Hello', 'I love you', 'Yes!']


        if (true) {
          setResponseOutput(dt[Math.floor(Math.random() * 3)])
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
      <div className='webcam'>
      <div id="rectangle"></div>
        <Webcam
          className='videoplayer'
          audio={false}
          height={500}
          ref={webcamRef}
          screenshotFormat="image/jpeg"
          width={800}
        />

      </div>
      
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
