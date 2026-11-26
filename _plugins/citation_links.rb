require "cgi"
require "jekyll/scholar"

module NaviDAM
  module CitationLinks
    module_function

    def doi_url(doi)
      value = doi.to_s.strip.sub(/\Adoi:\s*/i, "")
      return if value.empty?

      if value.match?(/\Ahttps?:\/\/(?:dx\.)?doi\.org\//i)
        value
      elsif value.match?(/\A(?:dx\.)?doi\.org\//i)
        "https://#{value}"
      else
        "https://doi.org/#{value}"
      end
    end

    def web_url(url)
      value = url.to_s.strip
      return if value.empty? || !value.match?(/\Ahttps?:\/\/\S+\z/i)

      value
    end

    def resource_url(doi, url)
      doi_url(doi) || web_url(url)
    end

    def anchor(url, label)
      return if url.to_s.empty?

      %(<a href="#{CGI.escapeHTML(url)}" target="_blank" rel="noopener noreferrer">#{CGI.escapeHTML(label)}</a>)
    end
  end

  module CitationLinkFilters
    def linkify_resource(reference, doi, url)
      rendered = reference.to_s
      doi_value = doi.to_s.strip.sub(/\Adoi:\s*/i, "")
      doi_target = CitationLinks.doi_url(doi)
      url_target = CitationLinks.web_url(url)

      rendered, doi_linked = linkify_value(rendered, doi_target, [doi_target, doi_value])
      rendered, url_linked = if url_target && url_target != doi_target
                               linkify_value(rendered, url_target, [url_target])
                             else
                               [rendered, false]
                             end

      if doi_target && !doi_linked
        "#{rendered} #{CitationLinks.anchor(doi_target, doi_target)}"
      elsif url_target && !url_linked
        "#{rendered} #{CitationLinks.anchor(url_target, url_target)}"
      else
        rendered
      end
    end

    private

    def linkify_value(reference, target, displays)
      return [reference, false] if target.nil?

      escaped_target = CGI.escapeHTML(target)
      if reference.include?(%(<a href="#{escaped_target}")) ||
         reference.include?(%(<a href='#{escaped_target}'))
        return [reference, true]
      end

      display = displays.compact.uniq.find do |candidate|
        reference.include?(candidate) || reference.include?(CGI.escapeHTML(candidate))
      end
      return [reference, false] if display.nil?

      display_html = reference.include?(display) ? display : CGI.escapeHTML(display)
      link = CitationLinks.anchor(target, display)
      [reference.sub(display_html) { link }, true]
    end
  end
end

Liquid::Template.register_filter(NaviDAM::CitationLinkFilters)

module Jekyll
  class Scholar
    class CitationAwareCiteTag < CiteTag
      def render(context)
        citation = super
        return citation unless citation_link_page?

        doi_links = keys.filter_map do |key|
          entry = bibliography[key]
          next unless entry

          doi = entry.doi if entry.has_field?("doi")
          url = entry.url if entry.has_field?("url")
          target = NaviDAM::CitationLinks.resource_url(doi, url)

          NaviDAM::CitationLinks.anchor(target, "↗")
        end
        return citation if doi_links.empty?

        %(#{citation} <span class="citation-doi-links">#{doi_links.join(" ")}</span>)
      end

      protected

      def citation_link_page?
        page = context.registers[:page]
        return false unless page.respond_to?(:[])

        layout = page["layout"].to_s
        categories = Array(page["categories"]).flatten.map(&:to_s)

        %w[method baserefs example].include?(layout) ||
          categories.any? { |category| %w[methods practices examples].include?(category) }
      end
    end

    class CiteResourceTag < CitationAwareCiteTag
      def render(context)
        citation = super
        return citation unless citation_link_page?

        titles = keys.filter_map do |key|
          entry = bibliography[key]
          next unless entry && entry.has_field?("title")

          title = liquidify(entry)["title"].to_s.strip
          title unless title.empty?
        end
        return citation if titles.empty?

        %(#{citation} <span class="citation-resource-title">— #{titles.join("; ")}</span>)
      end
    end
  end
end

Liquid::Template.register_tag("cite", Jekyll::Scholar::CitationAwareCiteTag)
Liquid::Template.register_tag("cite_resource", Jekyll::Scholar::CiteResourceTag)
