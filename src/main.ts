import './assets/pico.min.css'
import App from './App.svelte'

const app = new App({
  target: document.getElementById('app'),
})

export default app

declare global {
  interface Window {
    webkitSpeechRecognition: any;
  }
}