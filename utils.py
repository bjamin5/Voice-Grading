import db_connection as db
import pdb

class Review:
    def __init__(self, tuple):
        rec_id, review_id, company_name, product_id, product_name, return_type, is_recommended, review_date, review_title, username, years_of_use, quality_of_service_value, pricing_value, fits_needs_value, ease_of_use_value, full_review_text, review_text_sentiment, review_text_positive_sentiment, review_text_negative_sentiment, review_text_neutral_sentiment, review_text_mixed_sentiment, rating, past_tax_filing_method, how_hear_about_us, tax_filing_experience, category, topic, how_improve, tax_situation, location = tuple
        self.rec_id = str(rec_id) if rec_id is not None else '' 
        self.review_id = str(review_id) if review_id is not None else ''
        self.company_name = str(company_name) if company_name is not None else ''
        self.product_id = str(product_id) if product_id is not None else ''
        self.product_name = str(product_name) if product_name is not None else ''
        self.return_type = str(return_type) if return_type is not None else ''
        self.is_recommended = str(is_recommended) if is_recommended is not None else ''
        self.review_date = str(review_date) if review_date is not None else ''
        self.review_title = str(review_title) if review_title is not None else ''
        self.username = ''
        self.years_of_use = str(years_of_use) if years_of_use is not None else ''
        self.quality_of_service_value = str(quality_of_service_value) if quality_of_service_value is not None else ''
        self.pricing_value = str(pricing_value) if pricing_value is not None else ''
        self.fits_needs_value = str(fits_needs_value) if fits_needs_value is not None else ''
        self.ease_of_use_value = str(ease_of_use_value) if ease_of_use_value is not None else ''
        self.full_review_text = str(full_review_text) if full_review_text is not None else ''
        self.review_text_sentiment = str(review_text_sentiment) if review_text_sentiment is not None else ''
        self.review_text_positive_sentiment = str(review_text_positive_sentiment) if review_text_positive_sentiment is not None else ''
        self.review_text_negative_sentiment = str(review_text_negative_sentiment) if review_text_negative_sentiment is not None else ''
        self.review_text_neutral_sentiment = str(review_text_neutral_sentiment) if review_text_neutral_sentiment is not None else ''
        self.review_text_mixed_sentiment = str(review_text_mixed_sentiment) if review_text_mixed_sentiment is not None else ''
        self.rating = str(rating) if rating is not None else ''
        self.past_tax_filing_method = str(past_tax_filing_method) if past_tax_filing_method is not None else ''
        self.how_hear_about_us = str(how_hear_about_us) if how_hear_about_us is not None else ''
        self.tax_filing_experience = str(tax_filing_experience) if tax_filing_experience is not None else ''
        self.category = str(category) if category is not None else ''
        self.topic = str(topic) if category is not None else ''
        self.how_improve = str(how_improve) if how_improve is not None else ''
        self.tax_situation = str(tax_situation) if tax_situation is not None else ''
        self.location = str(location) if location is not None else ''
    
    def serialize_to_json(self):
        return {
            'rec_id' : self.rec_id,
            'review_id' : self.review_id,
            'company_name' : self.company_name,
            'product_id' : self.product_id,
            'product_name' : self.product_name,
            'return_type' : self.return_type,
            'is_recommended' : self.is_recommended,
            'review_date' : self.review_date,
            'review_title' : self.review_title,
            'years_of_use' : self.years_of_use,
            'quality_of_service_value' : self.quality_of_service_value,
            'pricing_value' : self.pricing_value,
            'fits_needs_value' : self.fits_needs_value,
            'ease_of_use_value' : self.ease_of_use_value,
            'full_review_text' : self.full_review_text,
            'review_text_sentiment' : self.review_text_sentiment,
            'review_text_positive_sentiment' : self.review_text_positive_sentiment,
            'review_text_negative_sentiment' : self.review_text_negative_sentiment,
            'review_text_neutral_sentiment' : self.review_text_neutral_sentiment,
            'review_text_mixed_sentiment' : self.review_text_neutral_sentiment,
            'rating' : self.rating,
            'past_tax_filing_method' : self.past_tax_filing_method,
            'how_hear_about_us' : self.how_hear_about_us,
            'tax_filing_experience' : self.tax_filing_experience,
            'category' : self.category,
            'topic' : self.topic,
            'how_improve' : self.how_improve,
            'tax_situation' : self.tax_situation,
            'location' : self.location,
        }



    

def load_reviews_from_aws(filters=None):
    query = create_query(filters)
    return db.execute_query(query, True, True, (), filters)

def create_query(filters):
    return f"""
            SELECT *
            FROM freetaxusa_review
            WHERE review_date between \'2022-06-00\' and \'2022-06-18\'"""

def create_filtering_query(filters):
    return f"""
        SELECT analytics.*
        FROM analytics
        JOIN category ON analytics.predicted_category_id = category.rec_id
        WHERE app_id = %(app_id)s
            {'AND analytics.model_version = %(model_version)s' if filters['model_version'] is not None else ''}
            {'AND analytics.source = %(source)s' if filters['source'] is not None else ''}
            {'AND analytics.predicted_category_id = %(predicted_category)s' if filters['predicted_category'] is not None else ''}
            {'AND analytics.actual_category_id = %(actual_category)s' if filters['actual_category'] is not None else ''}
            {'AND analytics.predicted_topic_id = %(predicted_topic)s' if filters['predicted_topic'] is not None else ''}
            {'AND analytics.actual_topic_id = %(actual_topic)s' if filters['actual_topic'] is not None else ''}
            {'AND analytics.category_probability >= %(from_category_percentage)s' if filters['from_category_percentage'] is not None else ''}
            {'AND analytics.category_probability <= %(to_category_percentage)s' if filters['to_category_percentage'] is not None else ''}
            {'AND analytics.topic_probability >= %(from_topic_percentage)s' if filters['from_topic_percentage'] is not None else ''}
            {'AND analytics.topic_probability <= %(to_topic_percentage)s' if filters['to_topic_percentage'] is not None else ''}
            {'AND DATE(analytics.create_timestamp) >= %(from_time)s' if filters['from_time'] is not None else ''}
            {'AND DATE(analytics.create_timestamp) <= %(to_time)s' if filters['to_time'] is not None else ''}
        ORDER BY predicted_category_id, predicted_topic_id
    """
