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
