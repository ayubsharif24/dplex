#include <ogdf/basic/graph_generators.h>
#include <ogdf/fileformats/GraphIO.h>
#include <ogdf/energybased/FMMMLayout.h>

using namespace ogdf;
 
int main(){
	Graph G;
	GraphAttributes GA(G);
	if (!GraphIO::read(G, "input_graph.gml")) {
		std::cerr << "Could not load input_graph.gml" << std::endl;
		return 1;
	}

	// For SVG output 
	for (node v : G.nodes){ GA.width(v) = GA.height(v) = 5.0; }
	
	FMMMLayout fmmm;
	fmmm.useHighLevelOptions(true);
	fmmm.unitEdgeLength(15.0);
	fmmm.newInitialPlacement(true);
	fmmm.qualityVersusSpeed(FMMMOptions::QualityVsSpeed::NiceAndIncredibleSpeed);
	// GorgeousAndEfficient 
	// BeautifulAndFast 	
	// NiceAndIncredible
	fmmm.fixedIterations(50);

	fmmm.call(GA);
	// GraphIO::write(GA, "output-energybased-graph-layout.gml", GraphIO::writeGML);
	GraphIO::write(GA, "output-energybased-graph-layout.svg", GraphIO::drawSVG);
	return 0;
}