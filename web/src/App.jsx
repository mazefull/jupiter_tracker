import { useState } from 'react'
import TaskMenu from "./components/TaskMenu.jsx";
import AuthForm from "./components/AuthForm.jsx";


function App() {
  const [count, setCount] = useState(0)

  return (
      <>
          <div
              style={{
                  backgroundImage:
                      'url("https://media.geeksforgeeks.org/' +
                      'wp-content/uploads/20201221222410/download3.png")',
                  height: "300px",
                  backgroundRepeat: "no-repeat"
              }}
          >
              <h1>HELLO</h1>
          </div>




          <TaskMenu/>

          <AuthForm />

      </>
  )
}

export default App
