# == Schema Information
#
# Table name: tweets
#
#  id         :bigint           not null, primary key
#  user_id    :bigint           not null
#  content    :text
#  parent_id  :integer
#  created_at :datetime         not null
#  updated_at :datetime         not null
#
class Tweet < ApplicationRecord
  belongs_to :user
  belongs_to :parent, class_name: 'Tweet', optional: true
  has_many :replies, class_name: 'Tweet', foreign_key: 'parent_id'
  has_many :user_likes, foreign_key: 'like'
  has_many :likers, through: :user_likes, source: :user

  validates :content, length: { maximum: 280 }

  accepts_nested_attributes_for :parent
  def parent_attributes=(attrs)
    self.parent = Tweet.find_by!(id: attrs[:id])
  rescue ActiveRecord::RecordNotFound
    # nothing
  end

  has_one_attached :tweet_pic
  validates :tweet_pic,
            content_type: { in: ['image/png', 'image/jpeg'], message: 'must be a PNG or JPEG' },
            dimension: { width: { max: 2000 },
                         height: { max: 2000 },
                         message: 'must be no larger than 2000x2000' },
            size: { less_than: 2.megabyte, message: 'must be less than 2MB' }
end
