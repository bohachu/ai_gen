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

questionForm.addEventListener('submit', async (e) => {
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
