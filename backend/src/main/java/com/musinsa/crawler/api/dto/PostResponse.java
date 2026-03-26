package com.musinsa.crawler.api.dto;

import com.musinsa.crawler.domain.entity.Post;
import lombok.Builder;
import lombok.Getter;

import java.time.LocalDateTime;
import java.util.List;

@Getter
@Builder
public class PostResponse {
    private Long postId;
    private Long brandId;
    private String platform;
    private String externalPostId;
    private String content;
    private List<String> hashtags;
    private int likes;
    private int comments;
    private long views;
    private LocalDateTime postedAt;
    private LocalDateTime crawledAt;

    public static PostResponse from(Post post) {
        return PostResponse.builder()
                .postId(post.getPostId())
                .brandId(post.getBrandId())
                .platform(post.getPlatform())
                .externalPostId(post.getExternalPostId())
                .content(post.getContent())
                .hashtags(post.getHashtags())
                .likes(post.getLikes())
                .comments(post.getComments())
                .views(post.getViews())
                .postedAt(post.getPostedAt())
                .crawledAt(post.getCrawledAt())
                .build();
    }
}
