import { useState } from 'react'
import TaskMenu from "./components/TaskMenu.jsx";


function App() {
  const [count, setCount] = useState(0)

  return (
      <>
          <TaskMenu/>


      </>
  )
}

export default App
