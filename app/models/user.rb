# == Schema Information
#
# Table name: users
#
#  id                     :bigint           not null, primary key
#  email                  :string           default(""), not null
#  encrypted_password     :string           default(""), not null
#  reset_password_token   :string
#  reset_password_sent_at :datetime
#  remember_created_at    :datetime
#  created_at             :datetime         not null
#  updated_at             :datetime         not null
#
class User < ApplicationRecord
  # Include default devise modules. Others available are:
  # :confirmable, :lockable, :timeoutable, :trackable and :omniauthable
  devise :database_authenticatable, :registerable,
         :recoverable, :rememberable, :validatable,
         :omniauthable, omniauth_providers: [:google_oauth2]
  validates :username, uniqueness: { case_sensitive: false, message: 'username has already been taken' },
                       length: { minimum: 4, maximum: 15, message: 'username must be between 4 and 15 characters' },
                       format: { with: /\A[a-zA-Z0-9_]+\z/,
                                 message: 'username can only contain letters, numbers, and underscores' },
                       presence: { message: 'username cannot be blank' }

  has_many :user_likes
  has_many :likes, through: :user_likes, source: :tweet
  has_many :following_relationships, class_name: 'UserFollowing', foreign_key: 'user_id'
  has_many :followers_relationships, class_name: 'UserFollowing', foreign_key: 'following'
  has_many :following, through: :following_relationships, source: :following
  has_many :followers, through: :followers_relationships, source: :user, foreign_key: 'following'
  has_many :tweets

  has_one_attached :avatar
  validates :avatar,
            content_type: { in: ['image/png', 'image/jpeg'], message: 'must be a PNG or JPEG' },
            dimension: { width: { max: 1200 },
                         height: { max: 1200 },
                         message: 'must be no larger than 1200x1200' },
            size: { less_than: 2.megabyte, message: 'must be less than 2MB' }

  validates :bio, length: { maximum: 140, message: 'must be less than 140 characters' }

  #disable mail
  #after_create -> { UserMailer.with(user: self).welcome_email.deliver_later }

  def self.from_google(u)
    create_with(uid: u[:uid], provider: 'google',
                username: "user_#{User.last.id + 1}",
                password: Devise.friendly_token[0, 20]).find_or_create_by!(email: u[:email])
  end
end
