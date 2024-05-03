class CreateUserLikes < ActiveRecord::Migration[7.1]
  def change
    create_table :user_likes do |t|
      t.references :user, null: false, foreign_key: true
      t.integer :like

      t.timestamps

      t.index %i[user_id like], unique: true
    end
  end
end
