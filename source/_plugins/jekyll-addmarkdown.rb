module Jekyll
  class DragonBlock < Liquid::Block
    def initialize(tag_name, text, tokens)
      super
    end
    require "kramdown"
    def render(context)
      content = super
      "<div class=\"dragons\">#{Kramdown::Document.new(content).to_html}</div>"
    end
  end
end
Liquid::Template.register_tag('dragons', Jekyll::DragonBlock)

module Jekyll
  class MarkdownBlock < Liquid::Block
    def initialize(tag_name, text, tokens)
      super
    end
    require "kramdown"
    def render(context)
      content = super
      "#{Kramdown::Document.new(content).to_html}"
    end
  end
end
Liquid::Template.register_tag('md', Jekyll::MarkdownBlock)