const questionForm = document.getElementById('question-form')
const questionInput = document.getElementById('question-input')
const responseContainer = document.getElementById('response-container')


let editor
require.config({
  paths: {
    vs: 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.30.1/min/vs',
  },
})
require(['vs/editor/editor.main'], function () {
  editor = monaco.editor.create(responseContainer, {
    language: 'python',
    theme: 'vs-dark',
    fontSize: 17,
  })
})

const askBtn = document.getElementById('ask-btn')
askBtn.addEventListener('click', async (e) => {
  e.preventDefault()

  const question = questionInput.value

  try {
    const response = await fetch('/ask', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ question }),
    })

    const reader = response.body.getReader()
    let decoder = new TextDecoder()
    let result = ''
    while (true) {
      const { value, done } = await reader.read()
      if (done) {
        break
      }
      result += decoder.decode(value)
      editor.setValue(result)
    }
  } catch (error) {
    editor.setValue('An error occurred. Please try again.')
  }
})

const runBtn = document.getElementById('run-btn')
runBtn.addEventListener('click', async (e) => {
  e.preventDefault()
  const html = editor.getValue() // 取得編輯器內容

  // 發送 HTTP POST 請求將 HTML 內容保存到後端
  try {
    const response = await fetch('/write_file', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        file_name: 'generated.html',
        path: './static/ai_gen',
        content: html,
      }),
    })

    const result = await response.json()
    if (result.status !== 'success') {
      throw new Error(result.message)
    }

    // 在新分頁中顯示 HTML 結果
    const newTab = window.open('/static/ai_gen/generated.html', '_blank') // 開啟新分頁
  } catch (error) {
    console.error(error)
    alert('An error occurred. Please try again.')
  }
})
