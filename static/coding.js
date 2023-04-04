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


// 新增按鈕點擊事件
const runBtn = document.getElementById('run-btn')
runBtn.addEventListener('click', () => {
  const html = editor.getValue() // 取得編輯器內容
  const parser = new DOMParser() // 建立 DOMParser
  const doc = parser.parseFromString(html, 'text/html') // 將 HTML 字串轉換成 DOM 物件
  const body = doc.querySelector('body') // 取得 body 元素

  // 將 HTML 結果顯示於 modal 中
  const modal = new bootstrap.Modal(document.getElementById('html-modal'))
  const iframe = document.getElementById('html-iframe')
  iframe.src = 'about:blank'
  iframe.contentWindow.document.open()
  iframe.contentWindow.document.write(body.innerHTML) // 將 body 元素內容寫入 iframe
  iframe.contentWindow.document.close()
  modal.show()
})