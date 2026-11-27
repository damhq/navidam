require "tmpdir"
require "fileutils"
require "jekyll"
require_relative "../_plugins/coverage_stats"

Dir.mktmpdir do |source|
  FileUtils.mkdir_p(File.join(source, "_data"))
  rows = [
    ["Good practices panel", "", "", "", "", "", "", "Examples"],
    ["Page name", "Author", "Status", "Reviewer", "Remarks", "", "", "Page name", "Author", "Status"],
    ["Reviewed practice", "", "Reviewed", "", "", "", "", "Online example", "", "Online"],
    ["Practice for review", "", "To review", "", "", "", "", "Invited example", "", "Invited"],
    ["Unwritten practice", "", "To do"],
    ["Invited practice", "", "Invited"],
    ["", "", "To do", "", "", "", "", "", "", "Online"]
  ]
  File.write(File.join(source, "_data", NaviDAM::RAW_PANELS),
             rows.map { |row| CSV.generate_line(row, col_sep: "\t") }.join)
  site = Struct.new(:source, :data).new(source, {})

  NaviDAM::CoverageGenerator.new.generate(site)

  expected_gp = {
    "reviewed" => 1, "toreview" => 1, "planned" => 1, "todo" => 1, "total" => 4,
    "review_list" => ["Practice for review"],
    "todo_list" => ["Unwritten practice"],
    "planned_list" => ["Invited practice"]
  }
  expected_ex = { "online" => 1, "planned" => 1, "total" => 2 }
  abort "Unexpected good-practice counts: #{site.data['coverage']['gp']}" unless site.data["coverage"]["gp"] == expected_gp
  abort "Unexpected example counts: #{site.data['coverage']['ex']}" unless site.data["coverage"]["ex"] == expected_ex
  expected_statuses = {
    "Reviewed practice" => "Reviewed",
    "Practice for review" => "To review",
    "Unwritten practice" => "To do",
    "Invited practice" => "Invited"
  }
  abort "Unexpected good-practice statuses: #{site.data['good_practice_status']}" unless site.data["good_practice_status"] == expected_statuses
end
