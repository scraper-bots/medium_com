import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
    static targets = ["textarea", "counter"]

    update() {
        let charCount = this.textareaTarget.value.length
        this.counterTarget.textContent = 280 - charCount
    }
}
