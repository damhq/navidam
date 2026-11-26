require "csv"
require "cgi"
require "yaml"

def assert(condition, message)
  abort message unless condition
end

site_dir = ARGV.fetch(0, "_site")
example = File.read(File.join(site_dir, "contents/examples/STOC_synthetic-controls/index.html"))
main = example[/<main\b[^>]*>(.*?)<\/main>/m, 1]
assert(main, "Example page has no main content")

%w[
  data
  temporal-monitoring-of-common-birds--stoc
  annual-land-cover-products--glc_fcs30d
  objectives
  detection-of-abrupt-landscape-changes
  bird-diversity-metric-shifts-attribution
  perspectives
  references
].each do |id|
  assert(main.match?(/<h[12]\b[^>]*\bid="#{Regexp.escape(id)}"/), "Example page is missing heading #{id}")
end
assert(main.include?("STOC is a standardized count protocol"), "Example page is missing data content")
assert(main.match?(/<div class="references-section">\s*<ol class="bibliography">\s*<li>/),
       "Example page is missing its bibliography")

criterion = File.read(File.join(site_dir, "tslength.html"))
criterion_main = criterion[/<main\b[^>]*>(.*?)<\/main>/m, 1]
assert(criterion_main, "Criterion page has no main content")
assert(criterion_main.match?(%r{<h1\b[^>]*>.*?</h1>\s*<div class="criterion-type-tags"[^>]*>.*?Ordinal.*?</div>}m),
       "Criterion type tag is not immediately after the first heading")
assert(criterion_main.match?(%r{</h1>\s*<div class="criterion-type-tags"[^>]*>.*?</div>\s*<[^/]}m),
       "Criterion page is missing content after its type tag")

def assert_documentation_actions(html, guide_url, page)
  footer = html[%r{<footer class="site-footer site-footer-with-actions">.*?</footer>}m]
  actions = footer && footer[%r{<div class="documentation-actions">.*?</div>}m]
  assert(actions && footer.index("documentation-actions") < footer.index("<strong>Contact</strong>"),
         "#{page} is missing sidebar documentation actions above Contact")
  assert(actions.scan("<a ").size == 2, "#{page} should have two documentation actions")
  assert(actions.include?(%q{href="https://github.com/damhq/navidam/issues/new/choose" target="_blank" rel="noopener noreferrer">Document/review page</a>}),
         "#{page} is missing the documentation issue link")
  assert(actions.include?(%(href="#{guide_url}" target="_blank" rel="noopener noreferrer">Contributing section</a>)),
         "#{page} is missing the documentation guide link")
  main = html[%r{<main\b[^>]*>.*?</main>}m]
  assert(main && !main.include?('class="documentation-actions"'), "#{page} duplicates documentation actions in the main content")
end

method_pages = Dir.glob(File.join(site_dir, "contents/methods/**/index.html")).select do |path|
  File.read(path).include?('<div class="method-header">')
end
assert(!method_pages.empty?, "No rendered method pages found")
method_pages.each do |path|
  assert_documentation_actions(File.read(path), "https://damhq.github.io/navidam/contributing/#document-method", path)
end

panel_rows = CSV.read(File.join(__dir__, "../_data/DetectionAttribution methods - Good practices _ Examples Panels.tsv"),
                      col_sep: "\t", encoding: "UTF-8").drop(2)
{
  "graphs" => "A primer on causal graphs",
  "box1" => "Beyond method selection",
  "colinearity" => "Colinear inputs",
  "usage_diagram" => "NaviDAM usage diagram"
}.each do |page, name|
  row = panel_rows.find { |r| r[0]&.strip == name }
  assert(row && row[2] && !row[2].strip.empty?, "#{name} has no status in the panels TSV")
  status = row[2].strip
  status_class = status.downcase.gsub(/\s+/, "-")
  html = File.read(File.join(site_dir, "contents/practices", page, "index.html"))
  badge = %(<span class="label doc-status-#{status_class}">#{CGI.escapeHTML(status)}</span>)
  assert(html.match?(%r{<div class="practices-header">.*?#{Regexp.escape(badge)}}m),
         "#{page} is missing its good-practice status badge")
  assert_documentation_actions(html, "https://damhq.github.io/navidam/contributing/#5-good-practices-and-examples-pages-", page)
end

contributing = File.read(File.join(site_dir, "contributing/index.html"))
nav = contributing[%r{<nav aria-label="Main" id="site-nav".*?</nav>}m]
assert(nav, "Contributing page is missing its sidebar")
nav_items = YAML.load_file(File.join(__dir__, "../_data/contributing_nav.yml"))
toc = contributing[%r{<nav aria-label="Contributing table of contents">.*?</nav>}m]
assert(toc, "Contributing page is missing its table of contents")
nav_items.each do |item|
  in_sidebar = nav.include?(%(/contributing/##{item['anchor']}"))
  assert(in_sidebar == (item["sidebar"] != false), "Incorrect sidebar visibility for #{item['title']}")
  assert(toc.include?(%(href="##{item['anchor']}")), "Table of contents is missing #{item['title']}")
  assert(contributing.include?(%(id="#{item['anchor']}")), "Sidebar target #{item['anchor']} does not exist")
end
assert(toc.scan("<li>").size == nav_items.size, "Table of contents must contain only main sections")
assert(nav.scan(%r{href="/contributing/#[^"]+"}).size == nav_items.count { |item| item["sidebar"] != false },
       "Sidebar must contain only the selected main sections")
main = contributing[%r{<main\b[^>]*>.*?</main>}m]
headings = main.scan(%r{<h2\b[^>]*>.*?</h2>}m).map { |h| h.gsub(/<[^>]+>/, " ").strip }
numbers = headings.filter_map { |heading| heading[/\A(\d+)\./, 1]&.to_i }
assert(numbers == (1..nav_items.size).to_a, "Contributing main sections are not numbered consecutively")
assert(contributing.include?('id="5-good-practices-and-examples-pages-"'), "Previous good-practice guide link is broken")
assert(File.read(method_pages.first).include?('/contributing/#where-help'), "Other pages are missing Contributing navigation")
sections = contributing.scan(%r{<details class="contribution-section"[^>]*>.*?</details>}m)
assert(sections.size >= 3, "Missing contribution list sections")
assert(sections.none? { |section| section.match?(/<details[^>]*\sopen(?:[=>\s])/) }, "Contribution lists must be collapsed by default")
assert(sections.all? { |section| section.include?("<summary>") && (section.include?('class="contribution-list"') || section.include?("<p>")) },
       "Contribution sections must retain their lists or empty-state messages")
practice_ids = %w[good-practices-to-create good-practices-to-review good-practices-planned]
practice_positions = practice_ids.map { |id| contributing.index(%(id="#{id}")) }
assert(practice_positions.none?(&:nil?) && practice_positions == practice_positions.sort,
       "Good-practice sections should be ordered to create, to review, then planned")
{
  "methods.html" => {
    ids: %w[method-assessments-to-review method-documentation-to-create method-documentation-to-review method-documentation-planned],
    guides: { "assess-method" => "assessment", "document-method" => "documentation" }
  },
  "practices.html" => { ids: practice_ids, guides: { "practices-examples" => "good practices" } }
}.each do |filename, expected|
  html = File.read(File.join(site_dir, filename))
  index_main = html[%r{<main\b[^>]*>.*?</main>}m]
  assert(index_main && index_main.index("Table of contents") && index_main.index("Where help is needed") &&
         index_main.index("Table of contents") < index_main.index("Where help is needed"),
         "#{filename} should show contribution sections below its table of contents")
  rendered_sections = index_main.scan(%r{<details class="contribution-section"[^>]*>.*?</details>}m)
  ids = rendered_sections.map { |section| section[/id="([^"]+)"/, 1] }
  assert(ids == expected[:ids], "#{filename} has incorrect contribution sections")
  expected[:guides].each do |anchor, label|
    assert(index_main.include?(%(<p>See the Contributing section on <a href="/contributing/##{anchor}">#{label}</a>.</p>)),
           "#{filename} is missing the contributing section link for #{label}")
  end
  rendered_sections.each do |section|
    id = section[/id="([^"]+)"/, 1]
    original = sections.find { |item| item.include?(%(id="#{id}")) }
    assert(section == original, "#{filename} has a different contribution list for #{id}")
  end
end
practice_sections = {
  "To review" => "good-practices-to-review",
  "To do" => "good-practices-to-create",
  "Invited" => "good-practices-planned"
}
practice_sections.each do |status, id|
  section = sections.find { |s| s.include?(%(id="#{id}")) }
  assert(section, "Missing good-practice section #{id}")
  names = panel_rows.select { |r| r[0] && r[2]&.strip == status }.map { |r| r[0].strip }
  assert(section.include?("(#{names.size})"), "#{id} has an incorrect count")
  names.each { |name| assert(section.include?(CGI.escapeHTML(name)), "#{id} is missing #{name}") }
  assert(!section.include?("<a "), "#{id} should not link unpublished pages") unless status == "To review"
end
review_section = sections.find { |s| s.include?('id="good-practices-to-review"') }
{
  "A primer on causal graphs" => "graphs",
  "Beyond method selection" => "box1",
  "Colinear inputs" => "colinearity",
  "NaviDAM usage diagram" => "usage_diagram"
}.each do |name, path|
  next unless panel_rows.any? { |r| r[0]&.strip == name && r[2]&.strip == "To review" }
  assert(review_section.include?(%(/contents/practices/#{path}/">#{CGI.escapeHTML(name)}</a>)),
         "Review list is missing the page link for #{name}")
end
assert(!example.include?('class="documentation-actions"'), "Example page should not have documentation actions")
