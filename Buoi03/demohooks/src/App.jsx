import { useEffect, useState } from 'react'
import './App.css'
import {MyContext, MyContextProvider} from './MyContext'
import {Home} from './components/Home'
import {Profile} from './components/Profile'


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

  const [comp, setComponent] = useState('HOME');
  return (
    <MyContextProvider>

      <div>
        <a onClick={() => setComponent('HOME')}>HOME</a> | 
        <a onClick={() => setComponent('PROFILE')}>PROFILE</a>
      </div>
      {(comp === 'HOME') ? <Home /> : <Profile/> }
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
    </MyContextProvider>
  )
}

export default App
