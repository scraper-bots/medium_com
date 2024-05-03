# == Schema Information
#
# Table name: user_followings
#
#  id         :bigint           not null, primary key
#  user_id    :bigint           not null
#  following  :integer
#  created_at :datetime         not null
#  updated_at :datetime         not null
#
require "test_helper"

class UserFollowingTest < ActiveSupport::TestCase
  # test "the truth" do
  #   assert true
  # end
end
