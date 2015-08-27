package us.kbase.kbasetrees.test;

import java.io.File;
import java.io.FileInputStream;
import java.util.Arrays;
import java.util.List;
import java.util.zip.GZIPInputStream;

import us.kbase.auth.AuthService;
import us.kbase.common.service.UObject;
import us.kbase.kbasegenomes.Genome;
import us.kbase.kbasetrees.SpeciesTreeBuilder;
import us.kbase.kbasetrees.Tree;

public class TreeServerBugFix20150827 {
	private static String ws2url = "https://kbase.us/services/ws/";
	private static String userId = "rsutormin";
	private static String pwd = "*****";
	private static String genomeWsName = "KBasePublicGenomesV5";

	public static void main(String[] args) throws Exception {
	    createSpeciesTreeCustom();
	}
	
    private static void createSpeciesTreeCustom() throws Exception {
        SpeciesTreeBuilder stb = new SpeciesTreeBuilder().init(new File("temp_files"), 
                new File("data"), genomeWsName, SpeciesTreeBuilder.createDefaultObjectStorage(ws2url));
        List<String> genomeRefs = Arrays.asList("myref");
        String token = AuthService.login(userId, pwd).getTokenString();
        final String filePath = "data/test/Escherichia_coli_str_K_12_substr_MG1655_NCBI.genome.json.gz";
        Tree ret = stb.placeUserGenomes(token, genomeRefs, false, false, 10, new SpeciesTreeBuilder.GenomeProvider() {
            @Override
            public Genome loadGenome(String token, String genomeRef) throws Exception {
                return UObject.getMapper().readValue(new GZIPInputStream(new FileInputStream(new File(filePath))), Genome.class);
            }
        });
        System.out.println(ret);
        // Tree [name=null, description=null, type=SpeciesTree, tree=(((kb|g.2590:5.5E-4,((kb|g.1870:0.0,kb|g.2136:0.0):5.5E-4,kb|g.30847:5.5E-4)0.801:5.5E-4)0.442:5.5E-4,kb|g.842:5.5E-4)0.548:2.7499999999999985E-4,(kb|g.3558:5.5E-4,(kb|g.24615:5.5E-4,((kb|g.0:0.0,kb|g.26314:0.0,user1:0.0):5.5E-4,kb|g.30896:5.5E-4)0.997:5.5E-4):5.5E-4)0.934:2.750000000000002E-4);, treeAttributes={cog_codes=["16","103","532","72","12","97","533","126","256","52","96","102","100","244","504","94","18","98","99","13","172","30","130","86","93","186","49","89","92","90","164","81","185","87","88","51","91","519","80","48","215","343","150","151","41","46","127","82","105"]}, defaultNodeLabels={kb|g.0=Escherichia coli K12, kb|g.1870=Escherichia coli str. K-12 substr. MG1655, kb|g.2136=Escherichia coli DH1, kb|g.24615=Escherichia coli J53, kb|g.2590=Escherichia coli BW2952, kb|g.26314=Escherichia coli W3110, kb|g.30847=Escherichia coli KTE42, kb|g.30896=Escherichia coli KTE197, kb|g.3558=Escherichia coli str. K-12 substr. MG1655star, kb|g.842=Escherichia coli str. K-12 substr. DH10B, user1=Escherichia coli str. K-12 substr. MG1655}, wsRefs={kb|g.0={g=[2150/2/7]}, kb|g.1870={g=[2150/2490/1]}, kb|g.2136={g=[2150/17118/1]}, kb|g.24615={g=[2150/26592/1]}, kb|g.2590={g=[2150/29396/1]}, kb|g.26314={g=[2150/30290/1]}, kb|g.30847={g=[2150/39858/1]}, kb|g.30896={g=[2150/39964/1]}, kb|g.3558={g=[2150/44306/1]}, kb|g.842={g=[2150/45896/1]}, user1={g=[myref]}}, kbRefs={kb|g.0={g=[kb|g.0]}, kb|g.1870={g=[kb|g.1870]}, kb|g.2136={g=[kb|g.2136]}, kb|g.24615={g=[kb|g.24615]}, kb|g.2590={g=[kb|g.2590]}, kb|g.26314={g=[kb|g.26314]}, kb|g.30847={g=[kb|g.30847]}, kb|g.30896={g=[kb|g.30896]}, kb|g.3558={g=[kb|g.3558]}, kb|g.842={g=[kb|g.842]}, user1={g=[user1]}}, leafList=[kb|g.0, kb|g.1870, kb|g.2136, kb|g.24615, kb|g.2590, kb|g.26314, kb|g.30847, kb|g.30896, kb|g.3558, kb|g.842, user1], additionalProperties={}]
    }
}
