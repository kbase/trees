
package us.kbase.cdmientityapi;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: fields_MeasurementDescription</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "id",
    "name",
    "description",
    "unitOfMeasure",
    "category",
    "source_id"
})
public class FieldsMeasurementDescription {

    @JsonProperty("id")
    private String id;
    @JsonProperty("name")
    private String name;
    @JsonProperty("description")
    private String description;
    @JsonProperty("unitOfMeasure")
    private String unitOfMeasure;
    @JsonProperty("category")
    private String category;
    @JsonProperty("source_id")
    private String sourceId;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("id")
    public String getId() {
        return id;
    }

    @JsonProperty("id")
    public void setId(String id) {
        this.id = id;
    }

    public FieldsMeasurementDescription withId(String id) {
        this.id = id;
        return this;
    }

    @JsonProperty("name")
    public String getName() {
        return name;
    }

    @JsonProperty("name")
    public void setName(String name) {
        this.name = name;
    }

    public FieldsMeasurementDescription withName(String name) {
        this.name = name;
        return this;
    }

    @JsonProperty("description")
    public String getDescription() {
        return description;
    }

    @JsonProperty("description")
    public void setDescription(String description) {
        this.description = description;
    }

    public FieldsMeasurementDescription withDescription(String description) {
        this.description = description;
        return this;
    }

    @JsonProperty("unitOfMeasure")
    public String getUnitOfMeasure() {
        return unitOfMeasure;
    }

    @JsonProperty("unitOfMeasure")
    public void setUnitOfMeasure(String unitOfMeasure) {
        this.unitOfMeasure = unitOfMeasure;
    }

    public FieldsMeasurementDescription withUnitOfMeasure(String unitOfMeasure) {
        this.unitOfMeasure = unitOfMeasure;
        return this;
    }

    @JsonProperty("category")
    public String getCategory() {
        return category;
    }

    @JsonProperty("category")
    public void setCategory(String category) {
        this.category = category;
    }

    public FieldsMeasurementDescription withCategory(String category) {
        this.category = category;
        return this;
    }

    @JsonProperty("source_id")
    public String getSourceId() {
        return sourceId;
    }

    @JsonProperty("source_id")
    public void setSourceId(String sourceId) {
        this.sourceId = sourceId;
    }

    public FieldsMeasurementDescription withSourceId(String sourceId) {
        this.sourceId = sourceId;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((((((((((((("FieldsMeasurementDescription"+" [id=")+ id)+", name=")+ name)+", description=")+ description)+", unitOfMeasure=")+ unitOfMeasure)+", category=")+ category)+", sourceId=")+ sourceId)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
