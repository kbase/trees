package us.kbase.kbasetrees.test;

import java.io.File;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

import junit.framework.Assert;

import org.forester.io.parsers.nhx.NHXParser;
import org.forester.phylogeny.Phylogeny;
import org.forester.phylogeny.PhylogenyNode;
import org.forester.phylogeny.iterators.PhylogenyNodeIterator;
import org.junit.Test;

import us.kbase.auth.AuthService;
import us.kbase.common.service.Tuple11;
import us.kbase.common.service.UObject;
import us.kbase.common.utils.FastaReader;
import us.kbase.kbasegenomes.Feature;
import us.kbase.kbasegenomes.Genome;
import us.kbase.kbasetrees.ConstructSpeciesTreeParams;
import us.kbase.kbasetrees.ObjectStorage;
import us.kbase.kbasetrees.Tree;
import us.kbase.kbasetrees.SpeciesTreeBuilder;
import us.kbase.workspace.GetObjectInfoNewParams;
import us.kbase.workspace.ListObjectsParams;
import us.kbase.workspace.ObjectData;
import us.kbase.workspace.ObjectIdentity;
import us.kbase.workspace.SaveObjectsParams;
import us.kbase.workspace.SubObjectIdentity;

public class SpeciesTreeBuilderTest {
	
	public static void main(String[] args) throws Exception {
		String ws2url = "https://kbase.us/services/ws/";
		String userId = "nardevuser1";
		String pwd = "nardevuser2";
		String wsId = "nardevuser1:home";
		List<String> genomeRefs = Arrays.asList(new String[] {
				wsId + "/Shewanella_ANA_3.genome",
				wsId + "/Shewanella_MR_7_uid58343.genome", 
				wsId + "/Burkholderia_383_uid58073.genome",
		});
		SpeciesTreeBuilder stb = new SpeciesTreeBuilder().init(
				new File("temp_files"), new File("data"), SpeciesTreeBuilder.createDefaultObjectStorage(ws2url));
		String token = AuthService.login(userId, pwd).getTokenString();
		Tree tree = stb.placeUserGenomes(token, genomeRefs, true, false, 4, stb.createDefaultGenomeProvider());
		System.out.println(tree.getTree());
	}
	
	@Test
	public void testOneGenome() throws Exception {
		FastaReader fr = new FastaReader(new File("data/test", "Shewanella_ANA_3_uid58347.fasta"));
		List<Feature> features = new ArrayList<Feature>();
		for (Map.Entry<String, String> entry : fr.readAll().entrySet())
			features.add(new Feature().withId(entry.getKey()).withProteinTranslation(entry.getValue()));
		String ref = "Shewanella_ANA_3_uid58347.genome";
		String genomeName = "Shewanella_ANA_3_uid58347";
		Tree tree = build(ref, genomeName, features);
		System.out.println("SpeciesTreeBuilderTest: " + relabelTree(tree.getTree(), tree.getDefaultNodeLabels()));
		@SuppressWarnings("unchecked")
		List<String> cogs = UObject.getMapper().readValue(tree.getTreeAttributes().get("cog_codes"), List.class);
		Assert.assertEquals(49, cogs.size());
		Assert.assertTrue(tree.getTree().contains("user1"));
		Assert.assertEquals(ref, tree.getWsRefs().get("user1").get("g").get(0));
		Assert.assertEquals(genomeName, tree.getDefaultNodeLabels().get("user1"));
	}
	
	private static Tree build(String genomeRef, String genomeName, 
			List<Feature> features) throws Exception {
		Map<String, Genome> ref2genome = new LinkedHashMap<String, Genome>();
		ref2genome.put(genomeRef, new Genome().withScientificName(genomeName)
				.withFeatures(features));
		return build(ref2genome);
	}
	
	private static Tree build(final Map<String, Genome> ref2genome) throws Exception {
		final Tree[] treeWrap = new Tree[] { null };
		final List<String> genomeKbIds = new ArrayList<String>();
		SpeciesTreeBuilder stb = new SpeciesTreeBuilder().init(
				new File("temp_files"), new File("data"), new ObjectStorage() {
					@Override
					public List<Tuple11<Long, String, String, String, Long, String, Long, String, String, Long, Map<String, String>>> saveObjects(
							String authToken, SaveObjectsParams params) throws Exception {
						treeWrap[0] = params.getObjects().get(0).getData().asClassInstance(Tree.class);
						return new ArrayList<Tuple11<Long, String, String, String, Long, String, Long, String, String, Long, Map<String, String>>>();
					}
					@Override
					public List<ObjectData> getObjects(String authToken,
							List<ObjectIdentity> objectIds) throws Exception {
						Genome genome = ref2genome.get(objectIds.get(0).getRef());
						return Arrays.asList(new ObjectData().withData(new UObject(genome)));
					}
					@Override
					public List<Tuple11<Long, String, String, String, Long, String, Long, String, String, Long, Map<String, String>>> listObjects(
							String authToken, ListObjectsParams params)
							throws Exception {
						List<Tuple11<Long, String, String, String, Long, String, Long, String, String, Long, Map<String, String>>> ret =
								new ArrayList<Tuple11<Long, String, String, String, Long, String, Long, String, String, Long, Map<String, String>>>();
						if (params.getSkip() > 0)
							return ret;
						for (int i = 0; i < genomeKbIds.size(); i++) {
							String kbId = genomeKbIds.get(i);
							ret.add(new Tuple11<Long, String, String, String, Long, String, Long, String, String, Long, Map<String, String>>()
									.withE7(1L).withE1(i + 1L).withE5(1L).withE2(kbId));
						}
						return ret;
					}					
					@Override
					public List<ObjectData> getObjectSubset(String authToken, List<SubObjectIdentity> objectIds) throws Exception {
						throw new IllegalStateException("Unsupported method");
					}
					@Override
					public List<Tuple11<Long, String, String, String, Long, String, Long, String, String, Long, Map<String, String>>> getObjectInfoNew(
							String authToken, GetObjectInfoNewParams params) throws Exception {
						throw new IllegalStateException("Unsupported method");
					}
				});
		genomeKbIds.addAll(stb.loadGenomeKbToNames().keySet());
		stb.run("token", new ConstructSpeciesTreeParams().withNewGenomes(new ArrayList<String>(ref2genome.keySet()))
				.withUseRibosomalS9Only(0L).withOutWorkspace("ws").withNearestGenomeCount(10L), "", "ws/123");
		return treeWrap[0];
	}
	
	private static String relabelTree(String tree, Map<String, String> replacements) throws Exception {
        NHXParser parser = new NHXParser();
        parser.setSource(tree);
        Phylogeny [] trees = parser.parse();
        StringBuilder relabeledTrees = new StringBuilder();
        for(int k=0; k<trees.length; k++) {
            for( final PhylogenyNodeIterator it = trees[k].iteratorPostorder(); it.hasNext(); ) {
            	PhylogenyNode node = it.next();
            	String replacement = replacements.get(node.getName());
            	if(replacement != null) {
            		node.setName(replacement);
            	}
            }
            relabeledTrees.append(trees[k].toNewHampshire());
        }
        return relabeledTrees.toString();
	}
}
