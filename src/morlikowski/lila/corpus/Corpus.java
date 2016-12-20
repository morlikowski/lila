package morlikowski.lila.corpus;

import java.util.List;

public abstract class Corpus {
	
	protected List<Document> documents;
	
	public abstract void load (String path);
	
	public List<Document> getDocuments() {
		return this.documents;
	}

}
