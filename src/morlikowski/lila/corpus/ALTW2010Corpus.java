package morlikowski.lila.corpus;

import java.io.BufferedReader;
import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.file.DirectoryStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;

public class ALTW2010Corpus extends Corpus {

	private static final int DOCID = 0;
	private static final int PRI_LANG = 1;
	private static final int SEC_LANG = 4;

	@Override
	public void load(String datasetPath) {
		Path dataset = Paths.get(datasetPath);
		this.documents = new LinkedList<>();
		Map<String, Set<String>> fileLabels = ALTW2010Corpus.readFileLabels(dataset);

		try (DirectoryStream<Path> datasetFiles = Files.newDirectoryStream(dataset)) {
			datasetFiles.forEach(file -> {
				String text = readFileText(file);
				String fileName = file.getFileName().toString();
				Set<String> labels = fileLabels.get(fileName);
				this.documents.add(new Document(labels, text));
			});
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}

	private static Map<String, Set<String>> readFileLabels(Path dataset) {
		String dirName = dataset.getFileName().toString();
		Path summary = dataset.getParent().resolve(dirName + "-summary");
		Map<String, Set<String>> fileLabels = new HashMap<>();

		try (BufferedReader reader = Files.newBufferedReader(summary)) {
			fileLabels = reader.lines().map(line -> line.split(","))
					.collect(Collectors.toMap(columns -> columns[DOCID], columns -> {
						Set<String> labels = new HashSet<>();
						labels.add(columns[PRI_LANG]);
						labels.add(columns[SEC_LANG]);
						return labels;
					}));
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

		return fileLabels;
	}

	private static String readFileText(Path file) {
		try {
			return new String(Files.readAllBytes(file), Charset.forName("UTF-8"));
		} catch (IOException e) {
			e.printStackTrace();
			return "";
		}
	}

}
