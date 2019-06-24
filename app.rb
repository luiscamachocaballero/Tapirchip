require 'sinatra'
class HelloWorld < Sinatra::Base
get '/' do
 "Hello, world!"
end
get '/:name' do
 "Hello, #{params[:name]}!"
end
end
