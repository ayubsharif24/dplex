# meson compile -vC build
project('ogdf_example', 'cpp')
ogdf_dep = dependency('ogdf', required : true)
executable('ogdf_layout', 'ogdf_example.cpp', dependencies : ogdf_dep)
