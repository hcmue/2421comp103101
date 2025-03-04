import { useEffect, useState } from 'react'
import './App.css'

function App() {
  const [count, setCount] = useState(0)
  const [name, setName] = useState('HCMUE');
  
  //Lúc nào cũng gọi (có bất kỳ thay đổi)
  useEffect(() => {
    console.log(`Đang render ${count} - ${name}`)
  });

  //Gọi lúc khởi tạo
  useEffect(()=> {
    console.log(`Gọi khi khởi tạo ${count} - ${name}`)
  }, []);

  //Gọi khi biến state thay đổi
  useEffect(()=> {
    console.log(`Gọi khi thay đổi name: ${count} - ${name}`)
  }, [name]);
  return (
    <>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <input onChange={(e) => {
          setName(e.target.value)
        }} />
        <br />
        <button onClick={() => setName('HCMUE ' + count)}>Change Name</button>
        <button onClick={() => setCount(count+1)}>+</button>
        <button onClick={() => setCount(count-1)}>-</button>
      </div>
      <p className="read-the-docs">
        Count: {count} | {name}
      </p>
    </>
  )
}

export default App
