import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
    static targets = ["unlikeButton", "likeButton", "likeCount"]

    connect() {
        console.log(this.likeCountTarget.textContent)
    }

    like() {
        this.likeCountTarget.textContent = parseInt(this.likeCountTarget.textContent) + 1
        this.unlikeButtonTarget.hidden = false
        this.likeButtonTarget.hidden = true
    }

    unlike() {
        this.likeCountTarget.textContent = parseInt(this.likeCountTarget.textContent) - 1
        this.unlikeButtonTarget.hidden = true
        this.likeButtonTarget.hidden = false
    }
}