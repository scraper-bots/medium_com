import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
    static targets = ["followButton", "unfollowButton"]

    follow() {
        this.followButtonTarget.hidden = true
        this.unfollowButtonTarget.hidden = false
    }

    unfollow() {
        this.followButtonTarget.hidden = false
        this.unfollowButtonTarget.hidden = true
    }
}
