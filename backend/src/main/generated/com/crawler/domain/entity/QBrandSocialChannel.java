package com.crawler.domain.entity;

import static com.querydsl.core.types.PathMetadataFactory.*;

import com.querydsl.core.types.dsl.*;

import com.querydsl.core.types.PathMetadata;
import javax.annotation.processing.Generated;
import com.querydsl.core.types.Path;


/**
 * QBrandSocialChannel is a Querydsl query type for BrandSocialChannel
 */
@Generated("com.querydsl.codegen.DefaultEntitySerializer")
public class QBrandSocialChannel extends EntityPathBase<BrandSocialChannel> {

    private static final long serialVersionUID = 393420119L;

    public static final QBrandSocialChannel brandSocialChannel = new QBrandSocialChannel("brandSocialChannel");

    public final NumberPath<Long> brandId = createNumber("brandId", Long.class);

    public final NumberPath<Long> channelId = createNumber("channelId", Long.class);

    public final StringPath channelUrl = createString("channelUrl");

    public final DateTimePath<java.time.LocalDateTime> createdAt = createDateTime("createdAt", java.time.LocalDateTime.class);

    public final StringPath platformId = createString("platformId");

    public final StringPath region = createString("region");

    public final DateTimePath<java.time.LocalDateTime> updatedAt = createDateTime("updatedAt", java.time.LocalDateTime.class);

    public QBrandSocialChannel(String variable) {
        super(BrandSocialChannel.class, forVariable(variable));
    }

    public QBrandSocialChannel(Path<? extends BrandSocialChannel> path) {
        super(path.getType(), path.getMetadata());
    }

    public QBrandSocialChannel(PathMetadata metadata) {
        super(BrandSocialChannel.class, metadata);
    }

}

